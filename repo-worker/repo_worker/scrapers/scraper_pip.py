from typing import List

from repo_worker.utils import TreeNode


class PipScraper(object):
    @staticmethod
    def list_packages(limit: int | None = None) -> List[str]:
        """Given a repository, return a list of its packages."""
        raise NotImplementedError

    @staticmethod
    def list_package_versions(package: str, limit: int | None = None) -> List[str]:
        """Given a repository and package, return a list of available versions."""
        raise NotImplementedError

    @staticmethod
    def generate_dependency_tree(package: str, version: str) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""
        raise NotImplementedError
