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
    # check if tree already exists
    if await find_tree(tx, repo_name, pkg_name, pkg_vers) is not None:
        await update(tx, repo_name, pkg_name, pkg_vers, pkg_dependencies)
    else:
        univ_hash = generate_universal_hash(
            repo_name,
            pkg_name,
            pkg_vers,
        )
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


async def update(
    tx: Transaction, repo_name: str, pkg_name: str, pkg_vers: str, pkg_dependencies: str
) -> None:
    univ_hash = generate_universal_hash(
        repo_name,
        pkg_name,
        pkg_vers,
    )
    async with tx.cursor() as cur:
        await cur.execute(
            """
                UPDATE dependencies
                set pkg_dependencies=%s WHERE univ_hash=%s
            """,
            (
                str(pkg_dependencies),
                univ_hash,
            ),
        )


async def find_tree(
    tx: Transaction, repo_name: str, pkg_name: str, pkg_vers: str
) -> str | None:
    univ_hash = generate_universal_hash(
        repo_name,
        pkg_name,
        pkg_vers,
    )
    async with tx.cursor() as cur:
        await cur.execute(
            """
                SELECT pkg_dependencies from dependencies
                WHERE univ_hash=%s
            """,
            (univ_hash,),
        )
        row = await cur.fetchone()
        if isinstance(row, tuple):
            return row[0]
        else:
            return None


async def find_tree_id(tx: Transaction, univ_hash: str) -> str | None:
    async with tx.cursor() as cur:
        await cur.execute(
            """
                SELECT pkg_dependencies from dependencies
                WHERE univ_hash=%s
            """,
            (univ_hash,),
        )
        row = await cur.fetchone()
        if isinstance(row, tuple):
            return row[0]
        else:
            return None


async def get_row_count(tx: Transaction) -> int:
    async with tx.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM dependencies")
        row = await cur.fetchone()
        return row[0]  # type: ignore


async def drop_all_rows(tx: Transaction) -> None:
    """Drop all table rows."""
    async with tx.cursor() as cur:
        await cur.execute("TRUNCATE dependencies RESTART IDENTITY CASCADE")


async def get_table(tx: Transaction) -> list[DEPENDENCY]:
    async with tx.cursor() as cur:
        await cur.execute("SELECT * FROM dependencies")
        rows = await cur.fetchall()
        return [DEPENDENCY(*row) for row in rows]
