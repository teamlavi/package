import asyncio
import json
import time

import httpx
import psycopg

from daos import cve, dependencies
from daos.database import get_db_tx
from utils import config


CACHE_CURSOR: str | None = None


class SemVer:
    major_vers: int
    minor_vers: int
    patch_vers: int

    def __init__(
        self, major_vers: int | str, minor_vers: int | str, patch_vers: int | str
    ):
        self.major_vers = int(major_vers)
        self.minor_vers = int(minor_vers)
        self.patch_vers = int(patch_vers)

    def __repr__(self) -> str:
        return f"{self.major_vers}.{self.minor_vers}.{self.patch_vers}"


async def wait_for_live(timeout: int = 60) -> None:
    """Wait for database to spin up."""
    start_t = time.time()
    while time.time() - start_t < timeout:
        is_up = await is_db_up()
        if is_up:
            return
        await asyncio.sleep(1)
    raise Exception(f"Failed to connect in {timeout}s")


async def is_db_up() -> bool:
    """Check if database is alive and responding."""
    try:
        async with await get_db_tx() as tx:
            async with tx.cursor() as cur:
                await cur.execute("SELECT 1")
                resp = await cur.fetchone()
                if resp != (1,):
                    raise Exception(f"Unexpected resp: {resp}")
                return True
    except psycopg.errors.OperationalError:
        return False


async def is_db_initialized() -> bool:
    return await is_table_initialized("cves") and await is_table_initialized(
        "dependencies"
    )


async def get_table_storage_size(table_name: str = "dependencies") -> str:
    if table_name == "dependencies":
        async with await get_db_tx() as tx:
            return await dependencies.get_table_storage_size(tx)
    elif table_name == "cves":
        async with await get_db_tx() as tx:
            return await cve.get_table_storage_size(tx)
    else:
        return f"unknown table '{table_name}'"


async def is_table_initialized(table: str = "cves") -> bool:
    """Return whether the database has been initialized yet."""
    if table == "cves":
        try:
            async with await get_db_tx() as tx:
                await cve.get_row_count(tx)
                return True
        except psycopg.errors.UndefinedTable:
            return False
    elif table == "dependencies":
        try:
            async with await get_db_tx() as tx:
                await dependencies.get_row_count(tx)
                return True
        except psycopg.errors.UndefinedTable:
            return False
    else:
        return False


async def initialize_database() -> None:
    """Initialize the database."""

    # Build the tables
    async with await get_db_tx() as tx:
        async with tx.cursor() as cur:
            if not await is_table_initialized("cves"):
                await cur.execute(
                    """
                        CREATE TABLE cves (
                            id SERIAL PRIMARY KEY,
                            cve_id VARCHAR(50) NOT NULL,
                            severity VARCHAR(50),
                            description TEXT,
                            cwe TEXT,
                            url TEXT NOT NULL,
                            repo_name VARCHAR(50) NOT NULL,
                            pkg_name VARCHAR(100) NOT NULL,
                            pkg_vers VARCHAR(50) NOT NULL,
                            univ_hash VARCHAR(200) NOT NULL,
                            first_patched_vers VARCHAR(50)
                        );
                        ALTER TABLE cves
                            ADD CONSTRAINT unique_sha_cve UNIQUE (cve_id, univ_hash);
                            """,
                )
            if not await is_table_initialized("dependencies"):
                await cur.execute(
                    """
                    CREATE TABLE dependencies (
                      univ_hash VARCHAR(200) PRIMARY KEY,
                      repo_name VARCHAR(50) NOT NULL,
                      pkg_name VARCHAR(100) NOT NULL,
                      pkg_vers VARCHAR(50),
                      pkg_dependencies TEXT NOT NULL
                    );
                    """,
                )


async def nuke_database() -> None:
    """Delete database tables."""

    # Delete each of the tables in sequence
    for table_name in ["cves", "dependencies"]:
        try:
            async with await get_db_tx() as tx:
                async with tx.cursor() as cur:
                    # Can't do server-side binding, don't let user input affect this
                    await cur.execute(f"DROP TABLE {table_name}")
        except Exception as e:
            print(f"Failed to delete table {table_name} - {str(e)}")


async def clear_database() -> None:
    """Clear database rows."""
    # Clear each of the tables in sequence
    async with await get_db_tx() as tx:
        if await is_table_initialized("cve"):
            await cve.drop_all_rows(tx)
        if await is_table_initialized("dependencies"):
            await dependencies.drop_all_rows(tx)


async def table_size(table: str) -> int:
    """Get the number of rows in the db."""
    if table == "cves":
        async with await get_db_tx() as tx:
            return await cve.get_row_count(tx)
    elif table == "dependencies":
        async with await get_db_tx() as tx:
            return await dependencies.get_row_count(tx)
    else:
        raise Exception(f"Table {table} is not expected to exist")


async def insert_single_vulnerability(
    cve_id: str,
    url: str,
    repo_name: str,
    pkg_name: str,
    pkg_vers: str,
    severity: str | None = None,
    description: str | None = None,
    cwe: str | None = None,
    first_patched_vers: str | None = None,
) -> bool:
    """Insert a single vulnerability into the db."""
    async with await get_db_tx() as tx:
        return await cve.create(
            tx=tx,
            cve_id=cve_id,
            severity=severity,
            description=description,
            cwe=cwe,
            url=url,
            repo_name=repo_name,
            pkg_name=pkg_name,
            pkg_vers=pkg_vers,
            first_patched_vers=first_patched_vers,
        )


async def insert_single_dependency_tree(
    repo_name: str, pkg_name: str, pkg_vers: str, pkg_dependencies: str
) -> None:
    """Insert a single vulnerability into the db."""
    async with await get_db_tx() as tx:
        await dependencies.create(
            tx=tx,
            repo_name=repo_name,
            pkg_name=pkg_name,
            pkg_vers=pkg_vers,
            pkg_dependencies=pkg_dependencies,
        )


async def get_single_dependency_tree(
    repo_name: str, pkg_name: str, pkg_vers: str
) -> str | None:
    """Insert a single vulnerability into the db."""
    async with await get_db_tx() as tx:
        return await dependencies.find_tree(
            tx=tx,
            repo_name=repo_name,
            pkg_name=pkg_name,
            pkg_vers=pkg_vers,
        )


async def delete_single_vulnerability(
    repo_name: str, pkg_name: str, pkg_vers: str, cve_id: str
) -> bool:
    """Delete a single vuln, return whether or not the deletion was necessary."""
    async with await get_db_tx() as tx:
        doomed_cve = await cve.find_by_repo_pkg_vers_cve(
            tx, repo_name, pkg_name, pkg_vers, cve_id
        )
        if not doomed_cve:
            return False
        await cve.delete(tx, doomed_cve)
    return True


async def list_package_versions_npm(
    package: str, limit: int | None = None
) -> list[SemVer]:
    """Given a repository and package, return a list of available versions."""
    try:
        resp = httpx.get(
            f"https://registry.npmjs.org/{package}",
        )
        resp.raise_for_status()
        version_list = list(json.loads(resp.text)["versions"])
        if isinstance(version_list, str) and "-" in version_list:
            return []
        elif isinstance(version_list, str):
            version_list = [version_list]
        elif isinstance(version_list[0], list):
            version_list = version_list[0]

        res_versions: list[SemVer] = []

        for vers in version_list:
            if limit is not None and len(res_versions) >= limit:
                break
            elif vers.replace(".", "").isnumeric():
                # checks if there are characters in version number
                while vers.count(".") < 2:
                    # if no minor or patch version included
                    vers += ".0"
                res_versions.append(SemVer(*vers.split(".")))
        return res_versions
    except Exception as e:
        print(f"Unable to interpret npm versions for {package}", e)
        return []


async def list_package_versions_pip(
    package: str, limit: int | None = None
) -> list[SemVer]:
    """Given a repository and package, return a list of available versions."""
    try:
        page2 = f"https://pypi.org/pypi/{package}/json"
        all_versions = json.loads(httpx.get(page2).text)["releases"].keys()

        res_versions: list[SemVer] = []
        for vers in all_versions:
            if limit is not None and len(res_versions) >= limit:
                break
            elif vers.replace(".", "").isnumeric():
                # checks if there are characters in version number
                while vers.count(".") < 2:
                    # if no minor or patch version included
                    vers += ".0"
                res_versions.append(SemVer(*vers.split(".")))
        return res_versions
    except Exception as e:
        print(f"Unable to interpret pip versions for {package}", e)
        return []


async def get_vers_less_than_eql(
    repo_name: str,
    pkg_name: str,
    major_vers: int | str,
    minor_vers: int | str,
    patch_vers: int | str,
) -> list[str]:
    if repo_name == "npm":
        all_vers = await list_package_versions_npm(pkg_name)
    elif repo_name == "pip":
        all_vers = await list_package_versions_pip(pkg_name)
    else:
        all_vers = []
    res: list[str] = []
    for vers in all_vers:
        if vers.major_vers < int(major_vers):
            res.append(str(vers))
        elif vers.major_vers == int(major_vers) and vers.minor_vers < int(minor_vers):
            res.append(str(vers))
        elif (
            vers.major_vers == int(major_vers)
            and vers.minor_vers == int(minor_vers)
            and vers.patch_vers <= int(patch_vers)
        ):
            res.append(str(vers))
    return res


async def get_vers_less_than(
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    if repo_name == "npm":
        all_vers = await list_package_versions_npm(pkg_name)
    elif repo_name == "pip":
        all_vers = await list_package_versions_pip(pkg_name)
    else:
        all_vers = []
    res: list[str] = []
    for vers in all_vers:
        if vers.major_vers < int(major_vers):
            res.append(str(vers))
        elif vers.major_vers == int(major_vers) and vers.minor_vers < int(minor_vers):
            res.append(str(vers))
        elif (
            vers.major_vers == int(major_vers)
            and vers.minor_vers == int(minor_vers)
            and vers.patch_vers < int(patch_vers)
        ):
            res.append(str(vers))
    return res


async def get_vers_greater_than_eql(
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    if repo_name == "npm":
        all_vers = await list_package_versions_npm(pkg_name)
    elif repo_name == "pip":
        all_vers = await list_package_versions_pip(pkg_name)
    else:
        all_vers = []
    res: list[str] = []
    for vers in all_vers:
        if vers.major_vers > int(major_vers):
            res.append(str(vers))
        elif vers.major_vers == int(major_vers) and vers.minor_vers > int(minor_vers):
            res.append(str(vers))
        elif (
            vers.major_vers == int(major_vers)
            and vers.minor_vers == int(minor_vers)
            and vers.patch_vers >= int(patch_vers)
        ):
            res.append(str(vers))
    return res


async def get_vers_greater_than(
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    if repo_name == "npm":
        all_vers = await list_package_versions_npm(pkg_name)
    elif repo_name == "pip":
        all_vers = await list_package_versions_pip(pkg_name)
    else:
        all_vers = []
    res: list[str] = []
    for vers in all_vers:
        if vers.major_vers > int(major_vers):
            res.append(str(vers))
        elif vers.major_vers == int(major_vers) and vers.minor_vers > int(minor_vers):
            res.append(str(vers))
        elif (
            vers.major_vers == int(major_vers)
            and vers.minor_vers == int(minor_vers)
            and vers.patch_vers > int(patch_vers)
        ):
            res.append(str(vers))
    return res


async def vers_exists(
    repo_name: str,
    pkg_name: str,
    major_vers: str | int,
    minor_vers: str | int,
    patch_vers: str | int,
) -> bool:
    if repo_name == "npm":
        all_vers = await list_package_versions_npm(pkg_name)
    elif repo_name == "pip":
        all_vers = await list_package_versions_pip(pkg_name)
    else:
        all_vers = []
    for vers in all_vers:
        if (
            vers.major_vers == int(major_vers)
            and vers.minor_vers == int(minor_vers)
            and vers.patch_vers == int(patch_vers)
        ):
            return True
    return False


# helper function for scrape_vulnerabilities()
# Queries package table to get list of versions
async def vers_range_to_list(
    repo_name: str, pkg_name: str, vers_range: str
) -> list[str]:
    """
    Converts a range of versions to a list of available versions in range
    verse_range format:
    https://docs.github.com/en/graphql/reference/objects#securityvulnerability
    """

    if "," in vers_range:
        # double-sided range - separate queries and find overlap
        # could make a new SQL query, but it'd be fairly long
        # This implementation doesn't require additional code to check for
        # inclusive/exclusive endpoints
        lower_bound, upper_bound = vers_range.split(", ")
        lower_list = await vers_range_to_list(repo_name, pkg_name, lower_bound)
        upper_list = await vers_range_to_list(repo_name, pkg_name, upper_bound)
        # return results inbetween edges
        return [vers for vers in lower_list if vers in upper_list]

    vri = vers_range.index(" ") + 1
    while not vers_range[vri:].replace(".", "").isnumeric():
        # TODO maybe another way to handle?
        # drop version extension
        vers_range = vers_range[:-1]

    if len(vers_range) == 0:
        # if all letters and drops the whole version_range in previous check
        return []

    while vers_range.count(".") < 2:
        # if no minor or patch version included
        vers_range += ".0"

    if vers_range.count(".") != 2:
        if vers_range[-2:] == ".0":
            return await vers_range_to_list(repo_name, pkg_name, vers_range[:-2])
        # TODO some releases have 4 version numbers
        print("EDGE CASE TO HANDLE", repo_name, pkg_name, vers_range)
        return []

    if vers_range[0] == "=":
        # only one version
        major_vers, minor_vers, patch_vers = vers_range[2:].split(".")
        if await vers_exists(repo_name, pkg_name, major_vers, minor_vers, patch_vers):
            return [vers_range[2:]]
        else:
            # TODO: any other handling here
            print(
                "Requesting version of package not in package database: "
                + pkg_name
                + " "
                + vers_range
            )
            return []
    elif vers_range[:2] == "<=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        return await get_vers_less_than_eql(
            repo_name, pkg_name, major_vers, minor_vers, patch_vers
        )
    elif vers_range[0] == "<":
        major_vers, minor_vers, patch_vers = vers_range[2:].split(".")
        return await get_vers_less_than(
            repo_name, pkg_name, major_vers, minor_vers, patch_vers
        )
    elif vers_range[:2] == ">=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        return await get_vers_greater_than_eql(
            repo_name,
            pkg_name,
            str(major_vers),
            str(minor_vers),
            str(patch_vers),
        )
    elif vers_range[0] == ">":
        major_vers, minor_vers, patch_vers = vers_range[2:].split(".")
        return await get_vers_greater_than(
            repo_name,
            pkg_name,
            str(major_vers),
            str(minor_vers),
            str(patch_vers),
        )
    else:
        return []


async def scrape_vulnerabilities(repository: str) -> None:
    """Scrape vulnerabilities from github, save to database."""
    global CACHE_CURSOR
    if repository not in ["npm", "pip"]:
        raise Exception(f"Unrecognized repo: {repository}")
    # Ran on repositories individually so that only relevant vulnerabilities are pulled
    # from GitHub
    auth_headers = {"Authorization": f"Bearer {config.GH_ACCESS_TOKEN}"}

    # Get vulnerabilities after:
    last_cursor = None  # = CACHE_CURSOR

    # Repeats until there are no new vulnerabilities
    # TODO: first:x how many to query at once?
    while True:
        query_type = (
            "securityVulnerabilities(first:100, ecosystem: "
            + repository.upper()
            + (
                ""
                if last_cursor is None or last_cursor == ""
                else ', after: "' + last_cursor + '"'  # type: ignore
            )
            + ", orderBy: {field: UPDATED_AT, direction: ASC})"
        )

        query = (
            """
            {"""
            + query_type
            + """
           {
            edges {
              cursor
              node {
                advisory {
                  cwes(first: 100) {
                    nodes {
                      cweId
                    }
                  }
                  summary
                  permalink
                  identifiers {
                    value
                    type
                  }
                }
                package {
                  name
                  ecosystem
                }
                severity
                updatedAt
                firstPatchedVersion{
                  identifier
                }
                vulnerableVersionRange
              }
            }
            pageInfo {
              endCursor
            }
          }
        }
        """
        )

        # Add authorization token to headers
        response = httpx.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers=auth_headers,
        )

        # Print returned JSON
        # print("response")
        # print(json.dumps(json.loads(response.text), indent=2))

        if '"message":"Bad credentials"' in response.text:
            print("GitHub Advisory Token Error")
            return
        elif "errors" in json.loads(response.text).keys():
            print("GitHub Advisory Query Error")
            return

        # Save for next query
        last_cursor = json.loads(response.text)["data"]["securityVulnerabilities"][
            "pageInfo"
        ]["endCursor"]

        if last_cursor is None:
            print("no newer vulns")
            return  # stop execution, no new data

        CACHE_CURSOR = last_cursor

        # Parse each vulnerability returned
        for gh_vuln_edge in json.loads(response.text)["data"][
            "securityVulnerabilities"
        ]["edges"]:
            vuln_cursor = gh_vuln_edge["cursor"]
            gh_vuln = gh_vuln_edge["node"]

            cve_id = next(
                (
                    item["value"]
                    for item in gh_vuln["advisory"]["identifiers"]
                    if item["type"] == "CVE"
                ),
                None,
            )
            if cve_id is None:
                # No CVE, don't add to database
                print("no cve id for " + vuln_cursor)
                continue

            severity = gh_vuln["severity"]
            description = gh_vuln["advisory"]["summary"]
            cwes = ",".join(
                [cwe_node["cweId"] for cwe_node in gh_vuln["advisory"]["cwes"]["nodes"]]
            )
            url = gh_vuln["advisory"]["permalink"]
            repo_name = gh_vuln["package"]["ecosystem"].lower()
            pkg_name = gh_vuln["package"]["name"]
            pkg_vers_range = gh_vuln["vulnerableVersionRange"]
            pkg_vers_list = await vers_range_to_list(
                repo_name, pkg_name, pkg_vers_range
            )
            try:
                first_patched_vers = gh_vuln["firstPatchedVersion"]["identifier"]
            except Exception:
                # Might not have a patched version
                first_patched_vers = None

            for release in pkg_vers_list:
                await insert_single_vulnerability(
                    cve_id,
                    url,
                    repo_name,
                    pkg_name,
                    release,
                    severity,
                    description,
                    cwes,
                    first_patched_vers,
                )
