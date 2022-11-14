from __future__ import annotations  # Postponed annotation evaluation, remove once 3.11

from base64 import b64encode
from hashlib import sha256
from typing import List


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

    def as_json(self) -> str:
        """Return the tree represented as json."""
        raise NotImplementedError


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
