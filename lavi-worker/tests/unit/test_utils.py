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


def _assert_trees_equal(
    tree1: Dict[str, List[str]], tree2: Dict[str, List[str]]
) -> None:
    """Whether two trees are equivalent."""
    if (tree1_k := set(tree1.keys())) != (tree2_k := set(tree2.keys())):
        raise Exception(f"Tree keys mismatch: {tree1_k} != {tree2_k}")

    for node in tree1_k:
        if (tree1_ck := set(tree1[node])) != (tree2_ck := set(tree2[node])):
            raise Exception(f"Children mismatch for {node}: {tree1_ck} != {tree2_ck}")


@pytest.mark.parametrize(
    "tree",
    [
        {
            "root": ["c1", "c2"],
            "c1": ["gc1", "gc2"],
            "c2": ["gc3"],
            "gc1": [],
            "gc2": [],
            "gc3": [],
        },
        {
            "f3IcSz56TBzuKXC7EdH3zQ9BM4OQAD2SdomsTMBj1rw=": [
                "tPuzLW5Plk3UdCa4q/+CTGCBtGWBYGq4Uqy+4RUbfY4=",
                "lOZqpDD3kvzgFYWXdVOCXZwMCZJCj4/MKCdyjSnD73I=",
            ],
            "tPuzLW5Plk3UdCa4q/+CTGCBtGWBYGq4Uqy+4RUbfY4=": [
                "jBTB2a6sTkvmDdcpOKCHNjpqJ7AiBW7x/SVrTiDHiVk="
            ],
            "jBTB2a6sTkvmDdcpOKCHNjpqJ7AiBW7x/SVrTiDHiVk=": [],
            "lOZqpDD3kvzgFYWXdVOCXZwMCZJCj4/MKCdyjSnD73I=": [
                "jBTB2a6sTkvmDdcpOKCHNjpqJ7AiBW7x/SVrTiDHiVk="
            ],
        },
        {
            "c1": ["gc1", "gc2"],
            "c2": ["gc3", "gc2"],
            "c3": ["gc3"],
            "c4": ["gc3"],
            "gc1": [],
            "ggc1": [],
            "gc2": [],
            "root": ["c1", "c2", "c3", "c4"],
            "gc3": ["ggc1"],
        },
    ],
)
def test_tree_compression(tree: Dict[str, List[str]]) -> None:
    """Test that compression and decompression are consistent."""
    compressed = utils.compress_tree(tree)
    decompressed = utils.decompress_tree(compressed)
    print(f"Tree Changes: {tree} -> {compressed} -> {decompressed}")
    _assert_trees_equal(tree, decompressed)
