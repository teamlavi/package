from __future__ import annotations  # Postponed annotation evaluation, remove once 3.11

from base64 import b64encode
from typing import Any

import orjson

from utils.utils import generate_universal_hash


class TreeNode(object):
    def __init__(
        self,
        repo: str,
        package: str,
        version: str,
        children: list[TreeNode] = [],
    ):
        """Build a tree node given a hash and children."""
        self.repo = repo
        self.package = package
        self.version = version
        self.children = [c for c in children]  # shallow copy necessary

    def add_child(self, child: TreeNode) -> None:
        """Add a child node."""
        self.children.append(child)

    def add_children(self, children: list[TreeNode]) -> None:
        """Add multiple children."""
        self.children.extend(children)

    def _as_json(self, all_nodes: dict[str, list[str]]) -> None:
        """Update the all_nodes with our children as necessary, recurse."""
        if (univ_hash := self.univ_hash()) in all_nodes:
            return  # This node has already been inserted

        # Add this node to the dict
        all_nodes[univ_hash] = list(set(child.univ_hash() for child in self.children))

        # Recurse to childrem
        for child in self.children:
            # Children will skip themselves if already inserted
            child._as_json(all_nodes)

    def as_json(self) -> str:
        """Return the tree represented as json."""
        # Enumerate every node in the tree into a hash table
        all_nodes: dict[str, list[str]] = {}
        self._as_json(all_nodes)
        return orjson.dumps(all_nodes).decode()

    def as_json_b64(self) -> str:
        """Return the tree represented as json and base64-encoded."""
        return b64encode(self.as_json().encode()).decode()

    def univ_hash(self) -> str:
        """Generate our universal hash."""
        return generate_universal_hash(self.repo, self.package, self.version)

    def __str__(self) -> str:
        """Get a string representation of the self."""
        # Don't recursively __str__ children bc it could be cyclic
        return (
            f'TreeNode(repo="{self.repo}", package="{self.package}", '
            f'version="{self.version}")'
        )


def generate_dependency_tree(
    cds: dict[str, Any],
) -> TreeNode:
    def get_node(
        univ_hash: str,
    ) -> TreeNode:
        """recursive function to generate tree"""
        cds_nodes = cds["nodes"]
        node_data = cds_nodes[univ_hash]
        children_list = node_data["dependencies"]
        # has children, generate them first
        children_node_list: list[TreeNode] = []
        for child_id in children_list:
            children_node_list.append(get_node(child_id))
        return TreeNode(
            cds["repository"],
            node_data["package"],
            node_data["version"],
            children_node_list,
        )

    return get_node(cds["root"]["dependencies"][0])
