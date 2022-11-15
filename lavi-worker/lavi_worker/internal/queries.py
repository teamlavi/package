from typing import List, Dict

from lavi_worker.daos import cve, package, dependencies
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


async def get_affected_packages(cve_univ_id: str) -> list[package.PACKAGE]:
    """Get list of affected packages"""
    return None

async def get_package_count() -> int:
    """Get number of packages in package database."""
    async with await get_db_tx() as tx:
        num = await package.get_row_count(tx)
    return num

async def get_dependencies(univ_id: str) -> None:
    """Get the list of dependencies for a package"""
    return None

async def get_vulnerable_package_count() -> int:
    """Get number of packages in package database with a vulnerability in the cve database."""
    async with await get_db_tx() as tx:
        return await cve.get_vulnerable_package_count(tx)

async def get_vulnerability_depth(univ_hash: str) -> Dict[str, list[int]]:
    """Get the depth of each vulnerability. """
    vulnerabilities: Dict[str, list[int]] = {}
    depth: int = 1
    async def get_vulnerabilities(rec_univ_hash: str, depth: int) -> Dict[str, list[int]]:
        async with await get_db_tx() as tx:
            deps: str = await dependencies.get_dependencies_id(tx, rec_univ_hash)
            for dep in deps:
                cves = find_full_vulnerabilities_id(rec_univ_hash)
                for cve in cves:
                    if cve.univ_id in vulnerabilities.keys:
                        vulnerabilities[cve.univ_id].append(depth)
                get_vulnerabilities(dep)


    
