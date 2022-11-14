from typing import Dict, List, Protocol

from repo_worker.scrapers.scraper_dud import DudScraper
from repo_worker.utils import TreeNode


class RepoScraper(Protocol):
    @staticmethod
    def list_packages(limit: int | None = None) -> List[str]:
        """Given a repository, return a list of its packages."""
        ...

    @staticmethod
    def list_package_versions(package: str, limit: int | None = None) -> List[str]:
        """Given a repository and package, return a list of available versions."""
        ...

    @staticmethod
    def generate_dependency_tree(package: str, version: str) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""
        ...


repo_scrapers: Dict[str, RepoScraper] = {
    "dud": DudScraper(),
}
