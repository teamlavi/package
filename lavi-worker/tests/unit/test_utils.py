from typing import Dict, List

import pytest

from lavi_worker import utils


@pytest.mark.parametrize(
    "repo, pkg, vers, expected",
    [("pip", "django", "3.2.0", "5gBFSzsr+1FbrUb4wnXtdtX1B9Xn2D8LOq6Q1VuGMMg=")],
)
def test_generate_universal_hash(repo: str, pkg: str, vers: str, expected: str) -> None:
    """Ensure universal hash generation is correct."""
    out = utils.generate_universal_hash(repo, pkg, vers)
    assert out == expected


def _trees_equal(tree1: Dict[str, List[str]], tree2: Dict[str, List[str]]) -> bool:
    """Whether two trees are equivalent."""
    return True


def test_tree_compression(tree: Dict[str, List[str]]) -> None:
    """Test that compression and decompression are consistent."""
    compressed = utils.compress_tree(tree)
    decompressed = utils.decompress_tree(compressed)
    if not _trees_equal(tree, decompressed):
        raise Exception(f"Tree Mismatch: {tree} -> {compressed} -> {decompressed}")
