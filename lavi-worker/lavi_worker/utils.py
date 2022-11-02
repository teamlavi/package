from enum import Enum
from hashlib import sha256


class RepoEnum(str, Enum):
    """Enumerate repository types."""

    pip = "pip"
    npm = "npm"
    golang = "golang"


def _sha256(content: str) -> str:
    """Wrapper for hashlib sha256."""
    return sha256(content.encode("UTF-8")).hexdigest()


def generate_universal_hash(repo: str, pkg: str, vers: str) -> str:
    """Generate the hash given the basic data."""
    return _sha256(_sha256(repo) + _sha256(pkg) + _sha256(vers))
