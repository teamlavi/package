from attrs import define

from lavi_worker.daos.database import Transaction
from lavi_worker.utils import generate_universal_hash


@define(frozen=True)
class DEPENDENCY:
    repo_name: str
    pkg_name: str
    pkg_vers: str
    univ_hash: str
    pkg_dependencies: str


async def create(
    tx: Transaction, repo_name: str, pkg_name: str, pkg_vers: str, pkg_dependencies: str
) -> None:
    univ_hash = generate_universal_hash(
        repo_name,
        pkg_name,
        pkg_vers,
    )
    # TODO: catch error if already exists
    async with tx.cursor() as cur:
        await cur.execute(
            """
                INSERT INTO dependencies
                VALUES (%s, %s, %s, %s, %s)
            """,
            (
                univ_hash,
                repo_name,
                pkg_name,
                pkg_vers,
                str(pkg_dependencies),
            ),
        )


async def get_row_count(tx: Transaction) -> int:
    async with tx.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM dependencies")
        row = await cur.fetchone()
        return row[0]  # type: ignore


async def drop_all_rows(tx: Transaction) -> None:
    """Drop all table rows."""
    async with tx.cursor() as cur:
        await cur.execute("TRUNCATE dependencies RESTART IDENTITY CASCADE")
