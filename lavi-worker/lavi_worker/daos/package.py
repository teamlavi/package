from attrs import define

from lavi_worker.daos.database import Transaction
from lavi_worker.utils import generate_universal_hash


@define(frozen=True)
class PACKAGE:
    repo_name: str
    pkg_name: str
    univ_hash: str
    major_vers: int
    minor_vers: int
    patch_vers: int
    num_downloads: int
    s3_bucket: str


async def create(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: int,
    minor_vers: int,
    patch_vers: int,
    num_downloads: int | None,
    s3_bucket: str | None,
) -> None:
    """Create a CVE object in the database, return nothing if successful."""
    univ_hash = generate_universal_hash(
        repo_name,
        pkg_name,
        str(major_vers) + "." + str(minor_vers) + "." + str(patch_vers),
    )
    async with tx.cursor() as cur:
        await cur.execute(
            """
                INSERT INTO package
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                univ_hash,
                repo_name,
                pkg_name,
                major_vers,
                minor_vers,
                patch_vers,
                num_downloads,
                s3_bucket,
            ),
        )


async def get_vers_less_than_eql(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    async with tx.cursor() as cur:
        await cur.execute(
            """
                SELECT major_vers,
                       minor_vers,
                       patch_vers
                FROM PACKAGE
                WHERE repo_name=%s AND pkg_name=%s
                  AND (major_vers<%s
                       OR (major_vers=%s
                           AND minor_vers<%s)
                       OR (major_vers=%s
                           AND minor_vers=%s
                           AND patch_vers <=%s))
            """,
            (
                repo_name,
                pkg_name,
                major_vers,
                major_vers,
                minor_vers,
                major_vers,
                minor_vers,
                patch_vers,
            ),
        )
        rows = await cur.fetchall()
        vers_list = []
        for r in rows:
            vers = str(r[0]) + "." + str(r[1]) + "." + str(r[2])
            vers_list.append(vers)
        return vers_list


async def get_vers_less_than(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    async with tx.cursor() as cur:
        await cur.execute(
            """
                SELECT major_vers,
                       minor_vers,
                       patch_vers
                FROM PACKAGE
                WHERE repo_name=%s AND pkg_name=%s
                  AND (major_vers<%s
                       OR (major_vers=%s
                           AND minor_vers<%s)
                       OR (major_vers=%s
                           AND minor_vers=%s
                           AND patch_vers <%s))
            """,
            (
                repo_name,
                pkg_name,
                major_vers,
                major_vers,
                minor_vers,
                major_vers,
                minor_vers,
                patch_vers,
            ),
        )
        rows = await cur.fetchall()
        vers_list = []
        for r in rows:
            vers = str(r[0]) + "." + str(r[1]) + "." + str(r[2])
            vers_list.append(vers)
        return vers_list


async def get_vers_greater_than_eql(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    async with tx.cursor() as cur:
        await cur.execute(
            """
                SELECT major_vers,
                       minor_vers,
                       patch_vers
                FROM PACKAGE
                WHERE repo_name=%s AND pkg_name=%s
                  AND (major_vers>%s
                       OR (major_vers=%s
                           AND minor_vers>%s)
                       OR (major_vers=%s
                           AND minor_vers=%s
                           AND patch_vers >=%s))
            """,
            (
                repo_name,
                pkg_name,
                major_vers,
                major_vers,
                minor_vers,
                major_vers,
                minor_vers,
                patch_vers,
            ),
        )
        rows = await cur.fetchall()
        vers_list = []
        for r in rows:
            vers = str(r[0]) + "." + str(r[1]) + "." + str(r[2])
            vers_list.append(vers)
        return vers_list


async def get_vers_greater_than(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> list[str]:
    async with tx.cursor() as cur:
        await cur.execute(
            """
                SELECT major_vers,
                       minor_vers,
                       patch_vers
                FROM PACKAGE
                WHERE repo_name=%s AND pkg_name=%s
                  AND (major_vers>%s
                       OR (major_vers=%s
                           AND minor_vers>%s)
                       OR (major_vers=%s
                           AND minor_vers=%s
                           AND patch_vers >%s))
            """,
            (
                repo_name,
                pkg_name,
                major_vers,
                major_vers,
                minor_vers,
                major_vers,
                minor_vers,
                patch_vers,
            ),
        )
        rows = await cur.fetchall()
        vers_list = []
        for r in rows:
            vers = str(r[0]) + "." + str(r[1]) + "." + str(r[2])
            vers_list.append(vers)
        return vers_list


async def vers_exists(
    tx: Transaction,
    repo_name: str,
    pkg_name: str,
    major_vers: str,
    minor_vers: str,
    patch_vers: str,
) -> bool:
    async with tx.cursor() as cur:
        await cur.execute(
            """
                SELECT COUNT(*)
                FROM PACKAGE
                WHERE repo_name=%s
                AND pkg_name=%s
                AND major_vers=%s
                AND minor_vers=%s
                AND patch_vers=%s
            """,
            (
                repo_name,
                pkg_name,
                major_vers,
                minor_vers,
                patch_vers,
            ),
        )
        row = await cur.fetchone()

        if isinstance(row, tuple):
            return int(row[0]) > 0
        else:
            return False


async def get_row_count(tx: Transaction) -> int:
    async with tx.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM package")
        row = await cur.fetchone()
        return row[0]  # type: ignore


async def drop_all_rows(tx: Transaction) -> None:
    """Drop all table rows."""
    async with tx.cursor() as cur:
        await cur.execute("TRUNCATE package RESTART IDENTITY CASCADE")
