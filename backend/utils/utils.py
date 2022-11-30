from base64 import b64encode
from enum import Enum
from hashlib import sha256


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
    items = [repo, pkg, vers]
    return ":".join(b64encode(item.encode()).decode() for item in items)


def compress_tree(tree: dict[str, list[str]]) -> str:
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


def decompress_tree(compressed: str) -> dict[str, list[str]]:
    """Take a compressed tree and convert back to a python object."""
    lines = compressed.split("\n")
    nodes = lines[0].split(",")  # list of nodes

    tree: dict[str, list[str]] = {node: [] for node in nodes}
    for dependency_str in lines[1:]:
        if not dependency_str:
            continue
        parent_index: str
        children_indices: str
        parent_index, children_indices = dependency_str.split(">")
        parent: str = nodes[int(parent_index)]  # get parent node
        children: list[str] = children_indices.split(",")
        children = [nodes[int(child)] for child in children]  # get children nodes
        tree[parent].extend(children)  # append children to parent dependencies
    return tree


def parse_version(version: str) -> tuple[int, int, int] | None:
    """Try to parse a version string into major, minor, patch version numbers."""
    subvers = version.split(".")
    if len(subvers) != 3 or not all(subver.isdigit() for subver in subvers):
        return None
    # Checking isdigit should make this try-except redundant, but who cares
    try:
        return tuple(subvers)  # type: ignore
    except Exception as e:
        print(f"Unexpected issue parsing version '{version}' - {str(e)}")
        return None


def get_recent_version(versions: list[str]) -> str:
    """Get the most recent version from a list."""
    # Parse strings into list of tuples
    all_parsed = [parse_version(version) for version in versions]
    parsed: list[tuple[int, int, int]] = [tup for tup in all_parsed if tup is not None]

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
