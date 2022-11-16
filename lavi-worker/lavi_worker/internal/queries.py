from typing import List, Dict

from lavi_worker.daos import cve, dependencies
from lavi_worker.daos.database import get_db_tx
from lavi_worker.utils import RepoEnum, decompress_tree


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


# 1
async def get_affected_packages(repo: RepoEnum, pkgs: list[str]) -> dict[str, int]:
    """Get number of affected packages. Includes self."""
    # get all pkgs and their cves
    vuln_pkgs: dict[str, list[cve.CVE]] = {}
    for pkg in pkgs:
        cves: list[cve.CVE] = await find_full_vulnerabilities_id(pkg)
        if cves:
            vuln_pkgs[pkg] = cves
    # get number of packages that depend on the list of vulnerable packages
    vuln_pkg_effect: dict[str, int] = {}
    async with await get_db_tx() as tx:
        dep_table: list[dependencies.DEPENDENCY] = await dependencies.get_repo_table(
            tx, repo.value
        )
    for dep_entry in dep_table:
        dep_tree: dict[str, list[str]] = decompress_tree(dep_entry.pkg_dependencies)
        for pkg in dep_tree.keys():
            if pkg in vuln_pkgs.keys():
                vuln_pkg_effect[pkg] = vuln_pkg_effect.setdefault(pkg, 0) + 1
    return vuln_pkg_effect


# 2
async def get_package_count(repo: RepoEnum) -> int:
    """Get number of packages in package database."""
    async with await get_db_tx() as tx:
        num: int = await dependencies.get_repo_row_count(tx, repo.value)
    return num


# 3
async def get_dependencies(univ_hash: str) -> Dict[str, list[str]] | None:
    """Get the list of dependencies for a package"""
    async with await get_db_tx() as tx:
        dep_string: str | None = await dependencies.find_tree_id(tx, univ_hash)
    if dep_string:
        dep_tree: Dict[str, list[str]] = decompress_tree(dep_string)
        return dep_tree
    else:
        return None


async def get_num_dependencies(univ_hashes: list[str]) -> dict[str, int]:
    """Get the number of dependencies for each package"""
    num_deps: dict[str, int] = {}
    for univ_hash in univ_hashes:
        deps: dict[str, list[str]] | None = await get_dependencies(univ_hash)
        if deps is not None:
            num_deps[univ_hash] = len(deps) - 1
    return num_deps


# 4
async def get_vulnerable_package_count(repo: RepoEnum) -> int:
    """Get number of packages in package database with a vulnerability
    in the cve database."""
    async with await get_db_tx() as tx:
        return await cve.get_vulnerable_package_count(tx, repo.value)


# 5
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


async def get_vulnerability_depths(
    univ_hashes: list[str],
) -> dict[str, dict[str, list[int]]]:
    """Get the depth(s) of each vulnerability for each package"""
    all_vuln_depths: dict[str, dict[str, list[int]]] = {}
    for univ_hash in univ_hashes:
        vulns: dict[str, list[int]] | None = await get_vulnerability_depth(univ_hash)
        if vulns is None:
            vulns = {}
        all_vuln_depths[univ_hash] = vulns
    return all_vuln_depths


# 6
async def get_num_downloads(univ_hashes: list[str]) -> dict[str, int]:
    """Get the number of downloads for a package."""
    return {univ_hash: 0 for univ_hash in univ_hashes}


# 7
async def get_pkg_severity(pkgs: list[str]) -> dict[str, list[str]]:
    """Get the severities of the package vulnerabilities."""
    pkg_severities: dict[str, list[str]] = {}
    for pkg in pkgs:
        vulns: list[str] = []
        for vuln in await find_full_vulnerabilities_id(pkg):
            if vuln.severity is not None:
                vulns.append(vuln.severity)
        pkg_severities[pkg] = vulns
    return pkg_severities


# 8
async def get_cwes(pkgs: list[str]) -> list[str]:
    """Get the cwe ids from the list of packages"""
    cwe_ids: set[str] = set()
    for pkg in pkgs:
        vulns = await find_full_vulnerabilities_id(pkg)
        for vuln in vulns:
            if vuln.cwe is not None:
                cwe_ids.add(vuln.cwe)
    return list(cwe_ids)


async def get_num_vulns_cwe(cwe_id: str) -> int:
    """Get the number of vulnerabilities with this cwe."""
    async with await get_db_tx() as tx:
        return await cve.get_cwe_num_cves(tx, cwe_id)


async def get_num_vulns_cwes(cwe_ids: list[str]) -> dict[str, int]:
    """Get the number of vulnerabilities for each cwe."""
    return {cwe_id: await get_num_vulns_cwe(cwe_id) for cwe_id in cwe_ids}


async def get_num_types(pkgs: list[str]) -> dict[str, int]:
    cwe_ids: list[str] = await get_cwes(pkgs)
    return await get_num_vulns_cwes(cwe_ids)


# 9
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


async def get_all_vulnerable_packages(repo: RepoEnum) -> list[str]:
    """Get all vulnerable packages in our database."""
    pkgs: list[str] = []
    async with await get_db_tx() as tx:
        dep_table: list[dependencies.DEPENDENCY] = await dependencies.get_repo_table(
            tx, repo.value
        )
    for dep in dep_table:
        if await check_vulnerable(dep.univ_hash):
            pkgs.append(dep.univ_hash)
    return pkgs
