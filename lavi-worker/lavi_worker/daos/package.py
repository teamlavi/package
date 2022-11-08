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
	pkg_vers_id: str,
	major_vers: int,
	minor_vers: int,
	patch_vers: int,
	num_downloads: int | None,
	s3_bucket: str | None
) -> None:
    """Create a CVE object in the database, return nothing if successful."""
    # TODO: check that row doesn't already exist OR catch resultant psycopg3 err
    async with tx.cursor() as cur:
        await cur.execute(
            """
                INSERT INTO packages
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
			repo_name,
			pkg_name,
			pkg_vers_id,
			major_vers,
			minor_vers,
			patch_vers,
			num_downloads,
			s3_bucket
            ),
        )


async def delete(tx: Transaction) -> None:
	# TODO: implement
	pass