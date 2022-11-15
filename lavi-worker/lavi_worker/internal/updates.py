import json
import os

import httpx
import psycopg

from lavi_worker.daos import cve
from lavi_worker.daos import package
from lavi_worker.daos import dependencies
from lavi_worker.daos.database import get_db_tx
from lavi_worker import config

CACHE_CURSOR: str | None = None


async def is_db_initialized() -> bool:
    return (
        await is_table_initialized("cves")
        and await is_table_initialized("package")
        and await is_table_initialized("dependencies")
    )


async def get_table_storage_size(table_name: str = "dependencies") -> str:
    if table_name == "dependencies":
        async with await get_db_tx() as tx:
            return await dependencies.get_table_storage_size(tx)
    elif table_name == "cves":
        async with await get_db_tx() as tx:
            return await cve.get_table_storage_size(tx)
    elif table_name == "package":
        async with await get_db_tx() as tx:
            return await package.get_table_storage_size(tx)
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
    elif table == "package":
        try:
            async with await get_db_tx() as tx:
                await package.get_row_count(tx)
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
                            univ_hash VARCHAR(100) NOT NULL,
                            first_patched_vers VARCHAR(50)
                        );
                        ALTER TABLE cves
                            ADD CONSTRAINT unique_sha_cve UNIQUE (cve_id, univ_hash);
                            """,
                )
            if not await is_table_initialized("package"):
                await cur.execute(
                    """
                        CREATE TABLE package (
                         univ_hash VARCHAR(100) PRIMARY KEY,
                         repo_name VARCHAR(50) NOT NULL,
                         pkg_name VARCHAR(100) NOT NULL,
                         major_vers INTEGER NOT NULL,
                         minor_vers INTEGER NOT NULL,
                         patch_vers INTEGER NOT NULL,
                         num_downloads INTEGER,
                         s3_bucket varchar(50)
                         );
                     """,
                )
            if not await is_table_initialized("dependencies"):
                await cur.execute(
                    """
                    CREATE TABLE dependencies (
                      univ_hash VARCHAR(100) PRIMARY KEY,
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
    for table_name in ["cves", "package", "dependencies"]:
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
        if await is_table_initialized("package"):
            await package.drop_all_rows(tx)
        if await is_table_initialized("dependencies"):
            await dependencies.drop_all_rows(tx)


async def table_size(table: str) -> int:
    """Get the number of rows in the db."""
    if table == "cves":
        async with await get_db_tx() as tx:
            return await cve.get_row_count(tx)
    elif table == "package":
        async with await get_db_tx() as tx:
            return await package.get_row_count(tx)
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


async def insert_single_package_version(
    repo_name: str,
    pkg_name: str,
    major_vers: int,
    minor_vers: int,
    patch_vers: int,
    num_downloads: int | None = None,
    s3_bucket: str | None = None,
) -> None:
    """Insert a single package version into the db."""
    async with await get_db_tx() as tx:
        await package.create(
            tx=tx,
            repo_name=repo_name,
            pkg_name=pkg_name,
            major_vers=major_vers,
            minor_vers=minor_vers,
            patch_vers=patch_vers,
            num_downloads=num_downloads,
            s3_bucket=s3_bucket,
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
        async with await get_db_tx() as tx:
            vers_in_db = await package.vers_exists(
                tx, repo_name, pkg_name, major_vers, minor_vers, patch_vers
            )
            if vers_in_db:
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
        async with await get_db_tx() as tx:
            return await package.get_vers_less_than_eql(
                tx, repo_name, pkg_name, major_vers, minor_vers, patch_vers
            )
    elif vers_range[0] == "<":
        major_vers, minor_vers, patch_vers = vers_range[2:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_less_than(
                tx, repo_name, pkg_name, major_vers, minor_vers, patch_vers
            )
    elif vers_range[:2] == ">=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_greater_than_eql(
                tx,
                repo_name,
                pkg_name,
                str(major_vers),
                str(minor_vers),
                str(patch_vers),
            )
    elif vers_range[0] == ">":
        major_vers, minor_vers, patch_vers = vers_range[2:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_greater_than(
                tx,
                repo_name,
                pkg_name,
                str(major_vers),
                str(minor_vers),
                str(patch_vers),
            )
    else:
        return []


async def scrape_pip_versions(pkg_name: str) -> None:
    page2 = f"https://pypi.org/pypi/{pkg_name}/json"

    versions = json.loads(httpx.get(page2).text)["releases"]
    version_list = []

    try:
        for key in versions:
            versionHelper = key.split(".")
            if len(versionHelper) == 2:
                versionHelper.append("0")
                version_list.append(versionHelper)

            if len(versionHelper) == 3:
                await insert_single_package_version(
                    "pip",
                    str(pkg_name.lower()),
                    int(versionHelper[0]),
                    int(versionHelper[1]),
                    int(versionHelper[2]),
                )
            else:
                pass
    except Exception:
        pass


async def scrape_pip_packages() -> None:
    # hardcode list to scrape
    for pkg_name in ["arches"]:
        await scrape_pip_versions(pkg_name)
    return
    client = httpx.Client(follow_redirects=True)
    page = client.get("https://pypi.org/simple")  # Getting page HTML through request
    # print(page.text)
    stringHelper = page.text.replace(" ", "")
    links = stringHelper.split("\n")
    for pkg_name in links[7:-2]:  # -2 for this
        try:
            # E203: formatter puts whitespace before : but flake8 doesn't want it
            pkg_name = pkg_name[
                pkg_name.find(">") + 1 : pkg_name.rfind("<")  # noqa: E203
            ]
            await scrape_pip_versions(pkg_name)
        except Exception:
            pass


async def scrape_npm_versions(pkg_name: str) -> None:
    if pkg_name[0] == "-":
        return
    try:
        cmd = "npm view " + pkg_name + "@* version --json"
        request = os.popen(cmd).read()
        version_list = json.loads(request)

        if isinstance(version_list, str) and "-" in version_list:
            return
        elif isinstance(version_list, str):
            version_list = [version_list]
        elif isinstance(version_list[0], list):
            version_list = version_list[0]

        for vers in version_list:
            major_vers, minor_vers, patch_vers = vers.split(".")
            await insert_single_package_version(
                "npm", pkg_name.lower(), major_vers, minor_vers, patch_vers
            )
    except Exception as e:
        print(f"Unable to interpret versions for {pkg_name}", e)


async def scrape_npm_packages() -> None:
    """Get versions for npm packages"""
    # TODO get all npm packages
    for pkg_name in ["express", "async", "lodash", "cloudinary", "axios"]:
        await scrape_npm_versions(pkg_name)


async def scrape_packages() -> None:
    """Scrape released versions for all packages in repos"""
    await scrape_pip_packages()
    await scrape_npm_packages()


async def scrape_vulnerabilities() -> None:
    """Scrape vulnerabilities from github, save to database."""
    global CACHE_CURSOR
    # Ran on repositories individually so that only relevant vulnerabilities are pulled
    # from GitHub
    for repository in ["npm"]:
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
                    [
                        cwe_node["cweId"]
                        for cwe_node in gh_vuln["advisory"]["cwes"]["nodes"]
                    ]
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
