import json
import os

import httpx
import psycopg

from lavi_worker.daos import cve
from lavi_worker.daos import package
from lavi_worker.daos.database import get_db_tx
from lavi_worker import config

CACHE_CURSOR: str | None = None


async def is_db_initialized() -> bool:
    """Return whether the database has been initialized yet."""
    # Just check if the main table has been made
    try:
        async with await get_db_tx() as tx:
            await cve.get_row_count(tx)
    except psycopg.errors.UndefinedTable:
        return False
    # Propogate any other unexpected errors
    return True


async def initialize_database() -> None:
    """Initialize the database."""
    assert not await is_db_initialized()

    # Build the tables
    async with await get_db_tx() as tx:
        async with tx.cursor() as cur:
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
                        pkg_name VARCHAR(50) NOT NULL,
                        pkg_vers VARCHAR(50) NOT NULL,
                        univ_hash VARCHAR(100) NOT NULL
                    );
                    ALTER TABLE cves
                        ADD CONSTRAINT unique_sha_cve UNIQUE (cve_id, univ_hash);
                    CREATE TABLE package (
                                univ_hash VARCHAR(100) PRIMARY KEY,
                                repo_name VARCHAR(50) NOT NULL,
                                pkg_name VARCHAR(50) NOT NULL,
                                major_vers INTEGER NOT NULL,
                                minor_vers INTEGER NOT NULL,
                                patch_vers INTEGER NOT NULL,
                                num_downloads INTEGER,
                                s3_bucket varchar(50)
                    );
                """,
            )


async def nuke_database() -> None:
    """Delete database tables."""
    assert await is_db_initialized()

    # Delete each of the tables in sequence
    for table_name in ["cves", "package"]:
        try:
            async with await get_db_tx() as tx:
                async with tx.cursor() as cur:
                    # Can't do server-side binding, don't let user input affect this
                    await cur.execute(f"DROP TABLE {table_name}")
        except Exception as e:
            print(f"Failed to delete table {table_name} - {str(e)}")


async def clear_database() -> None:
    """Clear database rows."""
    assert await is_db_initialized()

    # Clear each of the tables in sequence
    async with await get_db_tx() as tx:
        await cve.drop_all_rows(tx)
        await package.drop_all_rows(tx)


async def database_size(table: str) -> int:
    """Get the number of rows in the db."""
    if table == "cves":
        async with await get_db_tx() as tx:
            return await cve.get_row_count(tx)
    elif table == "package":
        async with await get_db_tx() as tx:
            return await package.get_row_count(tx)
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

    if "-" in vers_range:
        # TODO maybe another way to handle?
        # drop version extension
        vers_range = vers_range[: vers_range.index("-")]

    while vers_range.count(".") < 2:
        # if no minor or patch version included
        vers_range += ".0"

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


async def scrape_pip_packages() -> None:
    page = httpx.get("https://pypi.org/simple/")  # Getting page HTML through request
    stringHelper = page.text.replace(" ", "")
    links = stringHelper.split("\n")
    for pkg_name in links[7:100]:  # -2 for this
        pkg_name = pkg_name[(pkg_name.find(">") + 1) : pkg_name.rfind("<")]
        try:
            page2 = f"https://pypi.org/pypi/{pkg_name}/json"

            versions = json.loads(httpx.get(page2).text)["releases"]
            version_list = []

            for key in versions:
                versionHelper = key.split(".")
                if len(versionHelper) == 3:
                    version_list.append(versionHelper)
                elif len(versionHelper) == 2:
                    versionHelper.append("0")
                    version_list.append(versionHelper)
                await insert_single_package_version(
                    "pip",
                    pkg_name.lower(),
                    versionHelper[0],
                    versionHelper[1],
                    versionHelper[2],
                )
        except Exception:
            pass


async def scrape_npm_packages() -> None:
    """Get versions for npm packages"""
    for package_name in ["express", "async", "lodash", "cloudinary", "axios"]:
        if package_name[0] == "-":
            continue
        try:
            cmd = "npm view " + package_name + "@* version --json"
            request = os.popen(cmd).read()
            version_list = json.loads(request)

            if isinstance(version_list, str) and "-" in version_list:
                continue
            elif isinstance(version_list, str):
                version_list = [version_list]
            elif isinstance(version_list[0], list):
                version_list = version_list[0]

            for vers in version_list:
                major_vers, minor_vers, patch_vers = vers.split(".")
                await insert_single_package_version(
                    "npm", package_name.lower(), major_vers, minor_vers, patch_vers
                )
        except Exception as e:
            print(f"Unable to interpret versions for {package_name}", e)


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
            print("response")
            print(json.dumps(json.loads(response.text), indent=2))

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
                print(pkg_vers_range)
                print(pkg_vers_list)
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
                    )
