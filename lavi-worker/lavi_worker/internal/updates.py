import psycopg
import httpx
import json
import requests
from bs4 import BeautifulSoup
import os

from lavi_worker.daos import cve
from lavi_worker.daos import package
from lavi_worker.daos.database import get_db_tx

# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
GLOBAL_CACHE = {
    "gh_access_token": "",
}


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
            return await package.get_row_count(tx)
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
            repo_name = repo_name,
            pkg_name = pkg_name,
            major_vers = major_vers,
            minor_vers = minor_vers,
            patch_vers = patch_vers,
            num_downloads = num_downloads,
            s3_bucket = s3_bucket
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
    if vers_range[0] == "=":
        # only one version
        return [vers_range[2:]]
    elif vers_range[:2] == "<=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_less_than_eql(tx, pkg_name, major_vers, minor_vers, patch_vers)
    elif vers_range[0] == "<":
        major_vers, minor_vers, patch_vers = vers_range[2:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_less_than(tx, pkg_name, major_vers, minor_vers, patch_vers)
    elif vers_range[:2] == ">=" and "<" in vers_range:
        # assumes valid range
        lower, upper = vers_range[3:].replace(" < ", "").split(",")
        lower_major_vers, lower_minor_vers, lower_patch_vers = lower.split(".")
        upper_major_vers, upper_minor_vers, upper_patch_vers = upper.split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_inbetween(tx, pkg_name, lower_major_vers, lower_minor_vers, lower_patch_vers, upper_major_vers, upper_minor_vers, upper_patch_vers)
    elif vers_range[:2] == ">=":
        major_vers, minor_vers, patch_vers = vers_range[3:].split(".")
        async with await get_db_tx() as tx:
            return await package.get_vers_greater_than_eql(tx, pkg_name, str(major_vers), str(minor_vers), str(patch_vers))
    else:
        return ["Invalid Query"]


async def scrape_pip_packages() -> [str]:
    """Get versions for pip packages"""
    page = requests.get('https://www.pypi.org/simple%27') # Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser')

    links = soup.select("a")
    packageslst = []
    count = 0
    countExceptions = 0
    for anchor in links[:10]:
        try:
            helper = []
            helper.append("pip")
            temp = anchor['href']
            temp = temp[8:-1]
            helper.append(temp)
            page2 = f'https://pypi.python.org/pypi/%7Btemp%7D/json'
            releases = json.loads(requests.get(page2).text)['releases']
            # releases = json.loads(request.urlopen(page2).read())['releases']
            versionsLst = []
            for key in releases:
                y = key.split(".")
                if len(y) == 3:
                    versionsLst.append(y)
                elif len(y) == 2:
                    y.append('0')
                    versionsLst.append(y)
            count += 1
            helper.append(versionsLst)
            packageslst.append(helper)
        except:
            count += 1
            countExceptions += 1

    return packageslst

async def scrape_npm_packages() -> None:
    """Get versions for npm packages"""
    with open("npm-packages-w-vuln.txt", "r") as f:
        package_list = [p.replace("'", "") for p in f.read().split(", ")]

    for package in package_list:
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
                    "npm", package, major_vers, minor_vers, patch_vers, None, None
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
    for repository in ["pip"]:
        auth_headers = {"Authorization": f"Bearer {GLOBAL_CACHE['gh_access_token']}"}
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
        last_cursor = get_last_cursor()

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
            # print(json.dumps(json.loads(response.text), indent=2))

            # Save for next query
            last_cursor = json.loads(response.text)["data"]["securityVulnerabilities"][
                "pageInfo"
            ]["endCursor"]

            if last_cursor is None:
                print("no newer vulns")
                return  # stop execution, no new data

            save_last_cursor(last_cursor)

            # Parse each vulnerability returned
            # parsed_vulnerabilities = []
            for gh_vuln_edge in json.loads(response.text)["data"][
                "securityVulnerabilities"
            ]["edges"]:
                # parsed_vuln = {}
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
                pkg_vers = gh_vuln["vulnerableVersionRange"]

                for release in vers_range_to_list(pkg_vers):
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
