from typing import List

from repo_worker.utils import TreeNode


class DudScraper(object):
    """A scraper for the dud repository."""

    @staticmethod
    def list_packages(repo: str, limit: int | None = None) -> List[str]:
        """Given a repository, return a list of its packages."""
        return ["mypkg1", "mypkg2", "mypkg3", "mypkg4"]

    @staticmethod
    def list_package_versions(
        repo: str, package: str, limit: int | None = None
    ) -> List[str]:
        """Given a repository and package, return a list of available versions."""
        return ["1.2.3", "1.2.4", "1.2.5"]

    @staticmethod
    def generate_dependency_tree(repo: str, package: str, version: str) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""
        # Just make a lil diamond-shaped tree
        root = TreeNode(repo, package, version)

        # Other package names for nodes
        other_packages = ["mypkg1", "mypkg2", "mypkg3", "mypkg4"]
        other_packages.remove(package)

        # Make one of the three the bottom node in the diamond
        bottom_package = TreeNode(repo, other_packages.pop(), "1.2.3")

        # The other two other packages are the direct deps
        for child in other_packages:
            child_node = TreeNode(repo, child, "1.2.3", children=[bottom_package])
            root.add_child(child_node)

        return root
