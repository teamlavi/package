import psycopg

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
    univ_hash: str
    first_patched_vers: str | None


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
    first_patched_vers: str | None,
) -> bool:
    """Create a CVE object in the database"""
    univ_hash = generate_universal_hash(repo_name, pkg_name, pkg_vers)
    async with tx.cursor() as cur:
        try:
            await cur.execute(
                """
                    INSERT INTO cves
                    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    univ_hash,
                    first_patched_vers,
                ),
            )
            return True
        except psycopg.errors.lookup("23505"):  # UniqueViolation
            print("Entry in cves already exists", repo_name, pkg_name, pkg_vers, cve_id)
            return False


async def delete(tx: Transaction, cve: CVE) -> None:
    """Delete the given CVE from the db."""
    async with tx.cursor() as cur:
        await cur.execute(
            "DELETE FROM cves WHERE cve_id = %s OR univ_hash = %s",
            (cve.cve_id, cve.univ_hash),
        )


async def find_by_univ_hash(tx: Transaction, univ_hash: str) -> List[CVE]:
    """Find by the universal hash string."""
    # Query the database
    async with tx.cursor() as cur:
        await cur.execute(
            "SELECT * FROM cves WHERE univ_hash = %s",
            (univ_hash,),
        )
        raw_cves = await cur.fetchall()

    # Parse output into objects, return
    return [CVE(*raw_cve) for raw_cve in raw_cves]


async def find_pkg_vers(tx: Transaction, repo_name: str, pkg_name: str) -> List[str]:
    """Find by the universal hash string."""
    # Query the database
    async with tx.cursor() as cur:
        await cur.execute(
            "SELECT pkg_vers FROM cves WHERE pkg_name = %s AND repo_name = %s",
            (pkg_name, repo_name),
        )
        versions = await cur.fetchall()

    return [version[0] for version in versions]


async def find_by_repo_pkg_vers(
    tx: Transaction, repo_name: str, pkg_name: str, pkg_vers: str
) -> List[CVE]:
    """Find any entries by their repo, pkg, vers tuple."""
    univ_hash = generate_universal_hash(repo_name, pkg_name, pkg_vers)
    return await find_by_univ_hash(tx, univ_hash)


async def find_by_univ_hash_cve(
    tx: Transaction, univ_hash: str, cve_id: str
) -> CVE | None:
    """Check if a specific CVE applies to a specific universal hash."""
    # Query the database
    async with tx.cursor() as cur:
        await cur.execute(
            "SELECT * FROM cves WHERE univ_hash = %s AND cve_id = %s",
            (univ_hash, cve_id),
        )
        raw_cve = await cur.fetchone()

    # Parse output into object if appropriate, return
    return CVE(*raw_cve) if raw_cve else None


async def find_by_repo_pkg_vers_cve(
    tx: Transaction, repo_name: str, pkg_name: str, pkg_vers: str, cve_id: str
) -> CVE | None:
    """Check if a specific CVE applies to a specific repo, pkg, vers tuple."""
    univ_hash = generate_universal_hash(repo_name, pkg_name, pkg_vers)
    return await find_by_univ_hash_cve(tx, univ_hash, cve_id)


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


async def get_vulnerable_package_count(tx: Transaction) -> int:
    """Get a block of rows."""
    async with tx.cursor() as cur:
        await cur.execute("SELECT univ_hash FROM cves")
        univ_hashes = await cur.fetchall()
        return len({univ_hash[0] for univ_hash in univ_hashes})


async def get_cwe_severities(tx: Transaction, cwe: str) -> list[str] | None:
    """Get the severities of vulnerabilities with this cwe."""
    async with tx.cursor() as cur:
        await cur.execute("SELECT severity FROM cves WHERE cwe = %s", (cwe))
        severities = await cur.fetchall()
        return [severity[0] for severity in severities] if severities else None

async def get_cwe_num_cves(tx: Transaction, cwe: str) -> int | None:
    """Get the vulnerabilities with this cwe. """
    async with tx.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM cves WHERE cwe=%s", (cwe))
        num = await cur.fetchone()
        return num[0] if num else None
