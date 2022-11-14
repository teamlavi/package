from repo_worker.scrapers import repo_scrapers


def list_packages(repo: str, limit: int | None = None) -> None:
    """Handle CLI runs of list-packages"""
    scraper = repo_scrapers[repo]
    packages = scraper.list_packages(limit=limit)
    for package in packages:
        print(package)


def list_package_versions(repo: str, package: str, limit: int | None = None) -> None:
    """Handle CLI runs of list-package-versions."""
    scraper = repo_scrapers[repo]
    versions = scraper.list_package_versions(package=package, limit=limit)
    for version in versions:
        print(version)


def generate_tree(repo: str, package: str, version: str) -> None:
    """Handle CLI runs of generate-tree."""
    scraper = repo_scrapers[repo]
    tree = scraper.generate_dependency_tree(package=package, version=version)
    print(tree)
