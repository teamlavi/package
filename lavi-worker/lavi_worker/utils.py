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
    # TODO compress the tree
    return str(tree)


def decompress_tree(compressed: str) -> Dict[str, List[str]]:
    """Take a compressed tree and convert back to a python object."""
    # TODO decompress tree
    decompressed: Dict[str, List[str]] = json.loads(compressed.replace("'", '"'))
    return decompressed
