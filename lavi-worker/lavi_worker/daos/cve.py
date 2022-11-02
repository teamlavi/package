from typing import List

from attrs import define

from lavi_worker.daos.database import Transaction
from lavi_worker.utils import generate_universal_hash


# Not actually a DAO, but we're going for minimum viable product here.
# A more nuanced solution would fold all these methods into the object itself, and use
# psycopg3 data adaptation configuration to automatically generate objects from queries.


@define(frozen=True)
class CVE:
    _id: int
    cve_id: str
    severity: str | None
    description: str | None
    cwe: str | None
    url: str
    repo_name: str
    pkg_name: str
    pkg_vers: str
    pkg_vers_id: str


async def create(
    tx: Transaction,
    cve_id: str,
    severity: str | None,
    description: str | None,
    cwe: str | None,
    url: str,
    repo_name: str,
    pkg_name: str,
    pkg_vers: str,
) -> None:
    """Create a CVE object in the database, return nothing if successful."""
    pkg_vers_id = generate_universal_hash(repo_name, pkg_name, pkg_vers)
    # TODO: check that row doesn't already exist OR catch resultant psycopg3 err
    async with tx.cursor() as cur:
        await cur.execute(
            """
                INSERT INTO cves
                VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                cve_id,
                severity,
                description,
                cwe,
                url,
                repo_name,
                pkg_name,
                pkg_vers,
                pkg_vers_id,
            ),
        )


async def delete(tx: Transaction, cve: CVE) -> None:
    """Delete the given CVE from the db."""
    # TODO: assert the entry exists in the db before deleting
    async with tx.cursor() as cur:
        await cur.execute(
            "DELETE FROM cves WHERE cve_id = %s",
            (cve.cve_id,),
        )


async def find_by_univ_hash(tx: Transaction, pkg_vers_id: str) -> List[CVE]:
    """Find by the universal hash string."""
    # Query the database
    async with tx.cursor() as cur:
        await cur.execute(
            "SELECT * FROM cves WHERE pkg_vers_id = %s",
            (pkg_vers_id,),
        )
        raw_cves = await cur.fetchall()

    # Parse output into objects, return
    return [CVE(*raw_cve) for raw_cve in raw_cves]


async def find_by_repo_pkg_vers(
    tx: Transaction, repo_name: str, pkg_name: str, pkg_vers: str
) -> List[CVE]:
    """Find any entries by their repo, pkg, vers tuple."""
    pkg_vers_id = generate_universal_hash(repo_name, pkg_name, pkg_vers)
    return await find_by_univ_hash(tx, pkg_vers_id)


async def get_row_count(tx: Transaction) -> int:
    """Get how many rows there are (each row is one repo-pkg-vers-cve)."""
    async with tx.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM cves")
        row = await cur.fetchone()
        return row[0]  # type: ignore


async def drop_all_rows(tx: Transaction) -> None:
    """Drop all table rows."""
    async with tx.cursor() as cur:
        await cur.execute("TRUNCATE cves RESTART IDENTITY CASCADE")
