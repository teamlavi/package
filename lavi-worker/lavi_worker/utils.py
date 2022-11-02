from enum import Enum


class RepoEnum(str, Enum):
    """Enumerate repository types."""

    pip = "pip"
    npm = "npm"
    golang = "golang"
