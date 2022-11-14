from __future__ import annotations  # Postponed annotation evaluation, remove once 3.11

from base64 import b64encode
from hashlib import sha256
import logging
from typing import Dict, List, Tuple

import orjson


class TreeNode(object):
    def __init__(
        self,
        repo: str,
        package: str,
        version: str,
        children: List[TreeNode] = [],
    ):
        """Build a tree node given a hash and children."""
        self.repo = repo
        self.package = package
        self.version = version
        self.children = children

    def add_child(self, child: TreeNode) -> None:
        """Add a child node."""
        self.children.append(child)

    def add_children(self, children: List[TreeNode]) -> None:
        """Add multiple children."""
        self.children.extend(children)

    def _as_json(self, all_nodes: Dict[str, List[str]]) -> None:
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
        all_nodes: Dict[str, List[str]] = {}
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


def _sha256(content: str | bytes) -> bytes:
    """Wrapper for hashlib sha256."""
    if isinstance(content, str):
        return sha256(content.lower().encode("UTF-8")).digest()
    elif isinstance(content, bytes):
        return sha256(content).digest()
    else:
        raise Exception(f"Unrecognized content type: {type(content)}")


def generate_universal_hash(repo: str, pkg: str, vers: str) -> str:
    """Generate the hash given the basic data."""
    univ_hash: bytes = _sha256(_sha256(pkg) + _sha256(vers) + _sha256(repo))
    return b64encode(univ_hash).decode("UTF-8")


def parse_version(version: str) -> Tuple[int, int, int] | None:
    """Try to parse a version string into major, minor, patch version numbers."""
    subvers = version.split(".")
    if len(subvers) != 3 or not all(subver.isdigit() for subver in subvers):
        return None
    # Checking isdigit should make this try-except redundant, but who cares
    try:
        return tuple(subvers)  # type: ignore
    except Exception as e:
        logging.warning(f"Unexpected issue parsing version '{version}' - {str(e)}")
        return None


def get_recent_version(versions: List[str]) -> str:
    """Get the most recent version from a list."""
    # Parse strings into list of tuples
    all_parsed = [parse_version(version) for version in versions]
    parsed: List[Tuple[int, int, int]] = [tup for tup in all_parsed if tup is not None]

    # Find highest
    max_c1 = max(parsed, key=lambda row: row[0])[0]
    parsed = [row for row in parsed if row[0] == max_c1]
    max_c2 = max(parsed, key=lambda row: row[1])[1]
    parsed = [row for row in parsed if row[1] == max_c2]
    max_c3 = max(parsed, key=lambda row: row[2])[2]
    highest = f"{max_c1}.{max_c2}.{max_c3}"

    # Ensure correct and return
    if highest not in versions:
        raise Exception(f"Highest version {highest} not in set {versions}")

    return highest
