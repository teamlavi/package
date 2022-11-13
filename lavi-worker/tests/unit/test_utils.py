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
