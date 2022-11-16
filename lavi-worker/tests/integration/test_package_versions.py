import httpx

from .config import BASE_URL


def test_npm_versions():
    """Test that insertion of vulns works."""
    # Reset the database
    # TODO: don't reset it, just clear relevant entries
    try:
        httpx.post(f"{BASE_URL}/internal/database/nuke")
        httpx.post(f"{BASE_URL}/internal/database/init")
    except Exception:
        print("Failed to reset database pre-test (not critical)")
        pass

    # TODO: Make these cases not break as new versions released
    # TODO: Add cases for other packages
    test_subcases = [
        ("npm", "lodash", "< 0.0.1", []),  # Below range
        ("npm", "lodash", "> 100.100.100", []),  # Above range
        ("npm", "lodash", "= 1.3.1", ["1.3.1"]),  # Exact that exists
        ("npm", "lodash", "= 1.3.5", []),  # Exact that doesn't exist
        ("npm", "lodash", ">= 4.17.20", ["4.17.20", "4.17.21"]),  # Valid query
        ("npm", "lodash", "> 4.17.20", ["4.17.21"]),  # Valid query
        (
            "npm",
            "lodash",
            "> 4.17.10, <= 4.17.13",
            ["4.17.11", "4.17.12", "4.17.13"],
        ),  # Valid query
        (
            "npm",
            "lodash",
            ">= 4.17.10, < 4.17.13",
            ["4.17.10", "4.17.11", "4.17.12"],
        ),  # Valid query
        ("npm", "axios", "> 1.1.0, < 1.1.3", ["1.1.1", "1.1.2"]),  # Valid query
        ("pip", "axios", "> 1.1.0, < 1.1.3", []),  # Query for package in wrong repo
    ]

    # Verify test cases don't have duplicates
    for repo_name, pkg_name, vers, expected in test_subcases:
        if len(expected) != len(set(expected)):
            raise Exception(
                f"Test bad - duplicates in {repo_name, pkg_name, vers, expected}"
            )

    for repo_name, pkg_name, vers, expected in test_subcases:
        # Make the query
        query = {"repo_name": repo_name, "pkg_name": pkg_name, "vers_range": vers}
        resp = httpx.get(f"{BASE_URL}/internal/query_vers", params=query)

        # Ensure output well-formed
        resp.raise_for_status()
        parsed = resp.json()
        assert isinstance(parsed, list)

        # Ensure no duplicates
        out_set = set(parsed)
        assert len(out_set) == len(parsed)

        # Assert sets identical
        exp_set = set(expected)
        assert out_set == exp_set, f"out -> {out_set} != {exp_set} <- expected"
