#!/usr/bin/env python3

from typing import Dict, List, Protocol


class TreeNode(object):
    def __init__(self, univ_hash, children):
        """Build a tree node given a hash and children."""
        self.univ_hash = univ_hash
        self.children = children

    def add_child(self, child) -> None:
        """Add a child node."""
        self.children.append(child)

    def as_json(self) -> str:
        """Return the tree represented as json."""
        raise NotImplementedError


class RepoScraper(Protocol):
    @staticmethod
    def list_packages(repo: str) -> List[str]:
        """Given a repository, return a list of its packages."""

    @staticmethod
    def list_package_versions(repo: str, package: str) -> List[str]:
        """Given a repository and package, return a list of available versions."""

    @staticmethod
    def generate_dependency_tree(repo, package, version) -> TreeNode:
        """Given a repository, package, and version, return a conflict-free dep tree."""


supported_repos: Dict[str, RepoScraper] = {
    "npm": RepoScraper,
    "pypi": RepoScraper,
}
