from typing import List

from attrs import define

from lavi_worker.daos.database import Transaction
from lavi_worker.utils import generate_universal_hash


@define(frozen=True)
class PACKAGE:
    repo_name: str
    pkg_name: str
    pkg_vers_id: str
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
    # TODO: check that row doesn't already exist OR catch resultant psycopg3 err
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
        pkg_name: str,
        major_vers: str,
        minor_vers: str,
        patch_vers: str,
) -> [str]:
    async with tx.cursor() as cur:
        await cur.execute(
            """SELECT * from package WHERE pkg_name=%s AND 
        (major_vers<%s OR 
        (major_vers=%s AND minor_vers<%s) OR 
        (major_vers=%s AND minor_vers=%s and patch_vers <=%s))""", (
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
            vers = r[0]+"."+r[1]+"."+r[2]
            vers_list.append(vers)
        return vers_list

async def get_vers_less_than(
        tx: Transaction,
        pkg_name: str,
        major_vers: str,
        minor_vers: str,
        patch_vers: str,
) -> [str]:
    async with tx.cursor() as cur:
        await cur.execute(
            """SELECT * from package WHERE pkg_name=%s AND 
        (major_vers<%s OR 
        (major_vers=%s AND minor_vers<%s) OR 
        (major_vers=%s AND minor_vers=%s and patch_vers <%s))""",
            (
                pkg_name,
                major_vers,
                major_vers,
                minor_vers,
                major_vers,
                minor_vers,
                patch_vers,
            ),)
        rows = await cur.fetchall()
        vers_list = []
        for r in rows:
            vers = r[0]+"."+r[1]+"."+r[2]
            vers_list.append(vers)
        return vers_list


async def get_vers_greater_than(
        tx: Transaction,
        pkg_name: str,
        major_vers: str,
        minor_vers: str,
        patch_vers: str,
) -> [str]:
    async with tx.cursor() as cur:
        await cur.execute(
            """SELECT * from package WHERE pkg_name=%s AND 
        (major_vers>%s OR 
        (major_vers=%s AND minor_vers>%s) OR 
        (major_vers=%s AND minor_vers=%s and patch_vers >=%s))""",
            (
                pkg_name,
                major_vers,
                major_vers,
                minor_vers,
                major_vers,
                minor_vers,
                patch_vers,
            ),)
        rows = await cur.fetchall()
        vers_list = []
        for r in rows:
            vers = r[0]+"."+r[1]+"."+r[2]
            vers_list.append(vers)
        return vers_list


async def get_vers_inbetween(
        tx: Transaction, pkg_name:str,
        lower_major_vers: str, lower_minor_vers: str, lower_patch_vers: str,
        upper_major_vers: str, upper_minor_vers: str, upper_patch_vers: str
) -> [str]:
    async with tx.cursor() as cur:
        await cur.execute(
            # concats queries from ?= and < sections
            """SELECT * from package WHERE pkg_name=%s AND 
                (major_vers>%s OR 
                (major_vers=%s AND minor_vers>%s) OR 
                (major_vers=%s AND minor_vers=%s and patch_vers >=%s)) AND 
                (major_vers<%s OR 
                (major_vers=%s AND minor_vers<%s) OR 
                (major_vers=%s AND minor_vers=%s and patch_vers <%s))""",
            (
                pkg_name,
                lower_major_vers, lower_major_vers, lower_minor_vers, lower_major_vers, lower_minor_vers,
                lower_patch_vers,
                upper_major_vers, upper_major_vers, upper_minor_vers, upper_major_vers, upper_minor_vers,
                upper_patch_vers
            ),)
        rows = await cur.fetchall()
        vers_list = []
        for r in rows:
            vers = r[0]+"."+r[1]+"."+r[2]
            vers_list.append(vers)
        return vers_list

async def get_row_count(tx: Transaction) -> int:
    async with tx.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM package")
        row = await cur.fetchone()
        return row[0]  # type: ignore

async def drop_all_rows(tx: Transaction) -> None:
    """Drop all table rows."""
    async with tx.cursor() as cur:
        await cur.execute("TRUNCATE package RESTART IDENTITY CASCADE")