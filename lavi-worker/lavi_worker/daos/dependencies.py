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
