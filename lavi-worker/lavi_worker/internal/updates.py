import psycopg
import httpx
import json

from lavi_worker.daos import cve
from lavi_worker.daos.database import get_db_tx

# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
GitHub_access_token = ""


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
                        pkg_vers_id VARCHAR(100) NOT NULL
                    );
                    ALTER TABLE cves
                        ADD CONSTRAINT unique_sha_cve UNIQUE (cve_id, pkg_vers_id)
                """,
            )


async def nuke_database() -> None:
    """Delete database tables."""
    assert await is_db_initialized()

    # Delete each of the tables in sequence
    async with await get_db_tx() as tx:
        async with tx.cursor() as cur:
            await cur.execute("DROP TABLE cves")
            # ... more tables as added


async def clear_database() -> None:
    """Clear database rows."""
    assert await is_db_initialized()

    # Clear each of the tables in sequence
    async with await get_db_tx() as tx:
        await cve.drop_all_rows(tx)
        # ... more tables as added


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


async def scrape_vulnerabilities() -> None:
    """Scrape vulnerabilities from github, save to database."""
    # Ran on repositories individually so that only relevant vulnerabilities are pulled
    # from GitHub
    for repository in ["PIP"]:
        auth_headers = {"Authorization": "Bearer " + GitHub_access_token}
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
                + repository
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

                # TODO pkg_vers is range
                # TODO replace insert_single_vulnerability()?
                insert_single_vulnerability(
                    cve_id,
                    url,
                    repo_name,
                    pkg_name,
                    pkg_vers,
                    severity,
                    description,
                    cwes,
                )
