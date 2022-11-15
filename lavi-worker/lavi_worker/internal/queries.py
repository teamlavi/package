from typing import List, Dict

from lavi_worker.daos import cve, package, dependencies
from lavi_worker.daos.database import get_db_tx
from lavi_worker.utils import RepoEnum
import json


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


async def get_affected_packages(cve_pkg_univ_hash: str) -> list[str]:
    """Get list of affected packages"""
    pkgs: list[str] = []
    async with await get_db_tx() as tx:
        dep_table: list[dependencies.DEPENDENCY] = await dependencies.get_table(tx)
        for dep in dep_table:
            dep_tree: Dict[str, list[str]] = json.loads(dep.pkg_dependencies)
            if cve_pkg_univ_hash in dep_tree.keys():
                pkgs.append(dep.univ_hash)
    return pkgs


async def get_package_count() -> int:
    """Get number of packages in package database."""
    async with await get_db_tx() as tx:
        num = await package.get_row_count(tx)
    return num


async def get_dependencies(univ_hash: str) -> Dict[str, list[str]] | None:
    """Get the list of dependencies for a package"""
    async with await get_db_tx() as tx:
        dep_string: str | None = await dependencies.find_tree_id(tx, univ_hash)
    if dep_string:
        dep_tree: Dict[str, list[str]] = json.loads(dep_string)
        return dep_tree
    else:
        return None


async def get_vulnerable_package_count() -> int:
    """Get number of packages in package database with a vulnerability
    in the cve database."""
    async with await get_db_tx() as tx:
        return await cve.get_vulnerable_package_count(tx)


async def get_vulnerability_depth(univ_hash: str) -> Dict[str, list[int]] | None:
    """Get the depth(s) of each vulnerability. Vulnerabilities with multiple paths
    have the length of each path in the list."""
    vulnerabilities: Dict[str, list[int]] = {}
    dep_tree: Dict[str, list[str]] | None = await get_dependencies(univ_hash)
    if dep_tree is None:
        return None
    else:
        dep_tree2: Dict[str, list[str]] = dep_tree

        async def get_vulnerabilities(rec_univ_hash: str, depth: int) -> None:
            deps = dep_tree2[rec_univ_hash]
            for dep in deps:
                vulns: list[cve.CVE] = await find_full_vulnerabilities_id(dep)
                for vuln in vulns:
                    if vuln.cve_id in vulnerabilities.keys():
                        vulnerabilities[vuln.cve_id].append(depth)
                    else:
                        vulnerabilities[vuln.cve_id] = [depth]
                await get_vulnerabilities(dep, depth + 1)
            return None

        await get_vulnerabilities(univ_hash, 1)
        return vulnerabilities


async def get_num_downloads(univ_hash: str) -> int:
    """Get the number of downloads for a package."""
    return 0


async def get_cwe_severity(cwe_id: str) -> list[str] | None:
    """Get the severity of the cwe."""
    async with await get_db_tx() as tx:
        return await cve.get_cwe_severities(tx, cwe_id)


async def get_num_vulns_cwe(cwe_id: str) -> int:
    """Get the number of vulnerabilities with this cwe."""
    async with await get_db_tx() as tx:
        return await cve.get_cwe_num_cves(tx, cwe_id)


async def check_vulnerable(univ_hash: str) -> bool:
    """Check if there is a vulnerability in a package or its dependencies"""
    dep_tree: Dict[str, list[str]] | None = await get_dependencies(univ_hash)
    if dep_tree is None:
        return False
    else:
        for pkg in dep_tree.keys():
            if await find_full_vulnerabilities_id(pkg):
                return True
    return False


async def get_all_vulnerable_packages() -> list[str]:
    """Get all vulnerable packages in our database."""
    pkgs: list[str] = []
    async with await get_db_tx() as tx:
        dep_table: list[dependencies.DEPENDENCY] = await dependencies.get_table(tx)
        for dep in dep_table:
            if check_vulnerable(dep.univ_hash):
                pkgs.append(dep.univ_hash)
    return pkgs
