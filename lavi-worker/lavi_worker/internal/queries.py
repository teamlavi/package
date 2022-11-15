from typing import List

from lavi_worker.daos import cve
from lavi_worker.daos import dependencies
from lavi_worker.daos.database import get_db_tx
from lavi_worker.utils import RepoEnum


async def find_vulnerabilities_simple(
    repo: RepoEnum, package: str, version: str
) -> List[str]:
    """Find CVE ids only for a single repo, package, and version."""

    # Get cves from the database
    async with await get_db_tx() as tx:
        cves = await cve.find_by_repo_pkg_vers(tx, repo.value, package, version)

    # Get just the CVE ids from the objects
    return [cve.cve_id for cve in cves]


async def find_vuln_versions(repo: RepoEnum, package: str) -> List[str]:

    # Get list of versions of the package from the database
    async with await get_db_tx() as tx:
        vers = await cve.find_pkg_vers(tx, repo.value, package)

    # Remove duplicates
    return list(set(vers))


async def find_full_vulnerabilities_id(
    univ_id: str,
) -> List[cve.CVE]:
    """Find CVE data from a universal hash."""

    # Get cves from the database
    async with await get_db_tx() as tx:
        cves = await cve.find_by_univ_hash(tx, univ_id)
    return cves


async def get_table_storage_size(table_name: str = "dependencies") -> str:
    async with await get_db_tx() as tx:
        return await dependencies.get_table_storage_size(tx)
