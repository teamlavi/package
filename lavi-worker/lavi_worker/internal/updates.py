import psycopg

from lavi_worker.daos import cve
from lavi_worker.daos.database import get_db_tx


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
