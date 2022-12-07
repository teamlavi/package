from daos import cve, dependencies
from daos.database import get_db_tx
from utils.utils import RepoEnum, decompress_tree


async def find_vulnerabilities_simple(
    repo: RepoEnum, package: str, version: str
) -> list[str]:
    """Find CVE ids only for a single repo, package, and version."""

    # Get cves from the database
    async with await get_db_tx() as tx:
        cves = await cve.find_by_repo_pkg_vers(tx, repo.value, package, version)

    # Get just the CVE ids from the objects
    return [cve.cve_id for cve in cves]


async def find_vuln_versions(repo: RepoEnum, package: str) -> list[str]:

    # Get list of versions of the package from the database
    async with await get_db_tx() as tx:
        vers = await cve.find_pkg_vers(tx, repo.value, package)

    # Remove duplicates
    return list(set(vers))


async def find_full_vulnerabilities_id(
    univ_id: str,
) -> list[cve.Cve]:
    """Find CVE data from a universal hash."""

    # Get cves from the database
    async with await get_db_tx() as tx:
        cves = await cve.find_by_univ_hash(tx, univ_id)
    return cves


# 1
async def get_affected_packages(repo: RepoEnum, pkgs: list[str]) -> dict[str, int]:
    """Get number of affected packages. Includes self."""
    # get all pkgs and their cves
    vuln_pkgs: dict[str, list[cve.Cve]] = {}
    for pkg in pkgs:
        cves: list[cve.Cve] = await find_full_vulnerabilities_id(pkg)
        if cves:
            vuln_pkgs[pkg] = cves
    # get number of packages that depend on the list of vulnerable packages
    vuln_pkg_effect: dict[str, int] = {}
    async with await get_db_tx() as tx:
        dep_table: list[dependencies.Dependency] = await dependencies.get_repo_table(
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
async def get_dependencies(univ_hash: str) -> dict[str, list[str]] | None:
    """Get the list of dependencies for a package"""
    async with await get_db_tx() as tx:
        dep_string: str | None = await dependencies.find_tree_id(tx, univ_hash)
    if dep_string:
        dep_tree: dict[str, list[str]] = decompress_tree(dep_string)
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
async def get_vulnerability_depth(univ_hash: str) -> dict[str, list[int]] | None:
    """Get the depth(s) of each vulnerability. Vulnerabilities with multiple paths
    have the length of each path in the list."""
    vulnerabilities: dict[str, list[int]] = {}
    dep_tree: dict[str, list[str]] | None = await get_dependencies(univ_hash)
    if dep_tree is None:
        return None
    else:
        dep_tree2: dict[str, list[str]] = dep_tree

        async def get_vulnerabilities(rec_univ_hash: str, depth: int) -> None:
            deps = dep_tree2[rec_univ_hash]
            for dep in deps:
                vulns: list[cve.Cve] = await find_full_vulnerabilities_id(dep)
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
    dep_tree: dict[str, list[str]] | None = await get_dependencies(univ_hash)
    if dep_tree is None:
        return False
    else:
        for pkg in dep_tree.keys():
            cves: list[cve.Cve] = await find_full_vulnerabilities_id(pkg)
            if cves:
                return True
    return False


async def get_all_vulnerable_packages(repo: RepoEnum) -> list[str]:
    """Get all vulnerable packages in our database."""
    pkgs: list[str] = []
    async with await get_db_tx() as tx:
        dep_table: list[dependencies.Dependency] = await dependencies.get_repo_table(
            tx, repo.value
        )
    for i, dep in enumerate(dep_table):
        check_val: bool = await check_vulnerable(dep.univ_hash)
        if check_val:
            pkgs.append(dep.univ_hash)
        print(i)
    print(pkgs)
    return pkgs


async def get_affected_packages_cve(
    repo: RepoEnum, cve_ids: list[str]
) -> dict[str, int]:
    """Get number of affected packages from CVE."""
    # get all pkgs and their cves
    vuln_pkgs: dict[str, list[str]] = {}
    for cve_id in cve_ids:
        vuln_pkgs[cve_id, await cve.get_cve_pkgs(cve_id)]
    # get number of packages that depend on the list of vulnerable packages
    cve_effect: dict[str, int] = {}
    async with await get_db_tx() as tx:
        dep_table: list[dependencies.Dependency] = await dependencies.get_repo_table(
            tx, repo.value
        )
    for dep_entry in dep_table:
        dep_tree: dict[str, list[str]] = decompress_tree(dep_entry.pkg_dependencies)
        for pkg in dep_tree.keys():
            for cve_id in vuln_pkgs.keys():
                if pkg in vuln_pkgs[cve_id]:
                    cve_effect[cve_id] = cve_effect.setdefault(pkg, 0) + 1
    return cve_effect


# 10
async def get_vulnerability_paths(
    pkgs: list[str],
) -> dict[str, dict[str, list[list[str]]]]:
    vuln_paths: dict[str, dict[str, list[list[str]]]] = {}

    # helper function to process one package at a time
    async def package_paths(pkg: str) -> None:
        pkg_paths: dict[str, list[list[str]]] = {}
        pkg_tree: dict[str, list[str]] | None = await get_dependencies(pkg)

        # traverse the tree recursively to find vulnerable package paths
        async def tree_traversal(currDep: str, currPath: list[str]) -> None:
            newPath: list[str] = currPath.copy()
            newPath.append(currDep)

            # check if the current dependency has any direct vulnerabilities
            if await find_full_vulnerabilities_id(currDep):
                if currDep in pkg_paths:
                    pkg_paths[currDep].append(newPath)
                else:
                    pkg_paths.update({currDep: [newPath]})

            # only traverse child dependencies if this dependency hasn't been seen already, avoid repeat traversal
            if pkg_tree[currDep]:
                for subDep in pkg_tree[currDep]:
                    await tree_traversal(subDep, newPath)

        # check to make sure this package has a dependency tree
        if pkg_tree:
            await tree_traversal(pkg, [])
            vuln_paths.update({pkg: pkg_paths})

    for pkg in pkgs:
        await package_paths(pkg)

    return vuln_paths


# 11
async def get_all_pkgs() -> list[dependencies.Package]:
    """Get all packages from dependencies table"""
    async with await get_db_tx() as tx:
        pkgs: list[dependencies.Package] = await dependencies.get_all_packages(tx)
    print[pkgs]
    return pkgs


# 12
async def get_tree_depth(univ_hash_list: list[str]) -> list[int]:
    """Get the max depth of the dependency tree"""
    result = []

    async def get_depth(tree: dict, key: str) -> int:
        if tree.get(key) is None:
            return 1
        result = 0
        for pkg in tree.get(key):
            curr = await get_depth(tree, pkg)
            if curr > result:
                result = curr
        return 1 + result

    for univ_hash in univ_hash_list:
        dep_tree: dict[str, list[str]] | None = await get_dependencies(univ_hash)
        if dep_tree is None:
            result.append(0)
        else:
            result.append(await get_depth(dep_tree, list(dep_tree.keys())[0]))
    return result


async def get_all_package_dependency_num_repo(repo: RepoEnum) -> dict[str, int]:
    """Get the number of dependencies for every package in the database for a repository."""
    async with await get_db_tx() as tx:
        deps: list[dependencies.Dependency] = await dependencies.get_repo_table(
            tx, repo.value
        )
    return {
        dep.univ_hash: len(decompress_tree(dep.pkg_dependencies).keys()) for dep in deps
    }


async def get_all_package_dependency_num() -> dict[str, dict[str, int]]:
    """Get the number of dependencies for every package in every repository."""
    return {
        repo.value: await get_all_package_dependency_num_repo(repo) for repo in RepoEnum
    }
