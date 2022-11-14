def list_packages(repo: str, limit: int | None = None) -> None:
    """Handle CLI runs of list-packages"""
    raise NotImplementedError


def list_package_versions(repo: str, package: str, limit: int | None = None) -> None:
    """Handle CLI runs of list-package-versions."""
    raise NotImplementedError


def generate_tree(repo: str, package: str, version: str) -> None:
    """Handle CLI runs of generate-tree."""
    raise NotImplementedError
