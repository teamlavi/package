import psycopg
import httpx
import os
import json

from lavi_worker.daos import cve
from lavi_worker.daos import package
from lavi_worker.daos.database import get_db_tx
from lavi_worker import config

# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic


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
    async with await get_db_tx() as tx:
        async with tx.cursor() as cur:
            await cur.execute("DROP TABLE cves")
            await cur.execute("DROP TABLE package")


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
    # ... more tables as added
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
) -> None:
    """Insert a single vulnerability into the db."""
    async with await get_db_tx() as tx:
        await cve.create(
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
async def vers_range_to_list(pkg_name: str, vers_range: str) -> list[str]:
    """Converts a range of versions to a list of available versions in range"""
    # verse_range format - https://docs.github.com/en/graphql/reference/objects#securityvulnerability
    print(vers_range)

    if "," in vers_range:
        # TODO implement double sided range
        return []

    if "-" in vers_range:
        # TODO maybe another way to handle?
        # drop version extension
        vers_range = vers_range[: vers_range.index("-")]

    while vers_range.count(".") < 2:
        # if no minor or patch version included
        vers_range += ".0"

    if vers_range[0] == "=":
        # only one version
        return [vers_range[2:]]
    elif vers_range[:2] == "<=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_less_than_eql(
                tx, pkg_name, major_vers, minor_vers, patch_vers
            )
    elif vers_range[0] == "<":
        major_vers, minor_vers, patch_vers = vers_range[2:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_less_than(
                tx, pkg_name, major_vers, minor_vers, patch_vers
            )
    elif vers_range[:2] == ">=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_greater_than_eql(
                tx, pkg_name, str(major_vers), str(minor_vers), str(patch_vers)
            )
    else:
        return []


async def scrape_pip_packages() -> [str]:
    pass


async def scrape_npm_packages() -> None:
    """Get versions for npm packages"""
    for package in ["express", "async", "lodash", "cloudinary"]:
        if package[0] == "-":
            continue
        try:
            cmd = "npm view " + package + "@* version --json"
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
                    "npm", package, major_vers, minor_vers, patch_vers, 0, "0"
                )
        except:
            print("unable to interpret versions for: ", package)


async def scrape_packages() -> None:
    """Scrape released versions for all packages in repos"""
    await scrape_pip_packages()
    await scrape_npm_packages()


async def scrape_vulnerabilities() -> None:
    """Scrape vulnerabilities from github, save to database."""
    global GLOBAL_CACHE
    # Ran on repositories individually so that only relevant vulnerabilities are pulled
    # from GitHub
    for repository in ["npm"]:
        auth_headers = {"Authorization": f"Bearer {config.GH_ACCESS_TOKEN}"}
        last_cursor_file = "last_cursor_" + repository + ".txt"

        # Get and save cursor are functions incase decide to save somewhere else
        def get_last_cursor():
            try:
                # TODO can I persist this data without files?
                with open(last_cursor_file, "r+") as f:
                    return f.read()
            except FileNotFoundError:
                return None

        def save_last_cursor(last_cursor_received):
            with open(last_cursor_file, "w") as f:
                f.write(last_cursor_received)

        # Get vulnerabilities after:
        last_cursor = None  # get_last_cursor()

        # Repeats until there are no new vulnerabilities
        while True:
            query_type = (
                "securityVulnerabilities(first:100, ecosystem: "
                + repository.upper()
                + (
                    ""
                    if last_cursor is None or last_cursor == ""
                    else ', after: "' + last_cursor + '"'
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

            # Save for next query
            last_cursor = json.loads(response.text)["data"]["securityVulnerabilities"][
                "pageInfo"
            ]["endCursor"]

            if last_cursor is None:
                print("no newer vulns")
                return  # stop execution, no new data

            save_last_cursor(last_cursor)

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
                repo_name = gh_vuln["package"]["ecosystem"]
                pkg_name = gh_vuln["package"]["name"]
                pkg_vers_range = gh_vuln["vulnerableVersionRange"]
                pkg_vers_list = await vers_range_to_list(pkg_name, pkg_vers_range)
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
