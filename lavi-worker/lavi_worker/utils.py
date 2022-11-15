import json
from base64 import b64encode
from enum import Enum
from hashlib import sha256
from typing import Dict, List


class RepoEnum(str, Enum):
    """Enumerate repository types."""

    pip = "pip"
    npm = "npm"
    golang = "golang"


class ResponseEnum(str, Enum):
    """Enumartor for LAVA GET responses"""

    complete = "complete"
    failure = "failure"
    pending = "pending"


class LevelEnum(str, Enum):
    """Enumerator for vulnerability levels for use in LavaRequest"""

    direct = "direct"
    indirect = "indirect"
    both = "both"  # default if None


class StatusEnum(str, Enum):
    """Enumerator for vulnerability status for use in LavaRequest"""

    patched = "patched"
    active = "active"  # default if None
    allVul = "allVul"


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


def compress_tree(tree: Dict[str, List[str]]) -> str:
    """Compress a tree into a smaller data structure for storage."""
    nodes_str = ""  # comma seperated ordered list of nodes
    dependencies_str = ""
    nodes = list(tree.keys())  # ordered list of nodes
    for node in tree:
        dependencies = tree[node]
        nodes_str += node + ","
        # if node has no dependencies then there is no need to show that
        if len(dependencies) > 0:
            dependencies_str += str(nodes.index(node)) + ">"
            for depend in dependencies:
                dependencies_str += str(nodes.index(depend)) + ","
            dependencies_str = dependencies_str[:-1]  # remove last comma
            dependencies_str += "\n"
    if dependencies_str[-1:] == "\n":
        dependencies_str = dependencies_str[:-1]
    nodes_str = nodes_str[:-1]  # remove last comma
    return nodes_str + "\n" + dependencies_str


def decompress_tree(compressed: str) -> Dict[str, List[str]]:
    """Take a compressed tree and convert back to a python object."""
    lines = compressed.split("\n")
    nodes = lines[0].split(",")  # list of nodes

    tree = {node: [] for node in nodes}
    for dependency_str in lines[1:]:
        parent, children = dependency_str.split(">")
        parent = nodes[int(parent)]  # get parent node
        children = children.split(",")
        children = [nodes[int(child)] for child in children]  # get children nodes
        tree[parent].extend(children)  # append children to parent dependencies
    return tree
