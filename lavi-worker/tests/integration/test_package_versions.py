import httpx

from .config import BASE_URL


def test_npm_scraper():
    """Test that insertion of vulns works."""
    # Reset the database
    # TODO: don't reset it, just clear relevant entries
    try:
        httpx.post(f"{BASE_URL}/internal/database/nuke")
        httpx.post(f"{BASE_URL}/internal/database/init")
    except Exception:
        print("Failed to reset database pre-test (not critical)")
        pass

    # Run the npm scraper
    resp = httpx.post(f"{BASE_URL}/internal/trigger_npm_scrapper", timeout=30.0)
    resp.raise_for_status()

    # TODO: Make these cases not break as new versions released
    # TODO: Add cases for other packages
    test_subcases = [
        ("lodash", "< 0.0.1", []),  # Below range
        ("lodash", "> 100.100.100", []),  # Above range
        ("lodash", "= 1.3.1", ["1.3.1"]),  # Exact that exists
        ("lodash", "= 1.3.5", []),  # Exact that doesn't exist
        ("lodash", ">= 4.17.20", ["4.17.20", "4.17.21"]),  # Valid query
        ("lodash", "> 4.17.20", ["4.17.21"]),  # Valid query
    ]

    # Verify test cases don't have duplicates
    for pkg_name, vers, expected in test_subcases:
        if len(expected) != len(set(expected)):
            raise Exception(f"Test bad - duplicates in {pkg_name, vers, expected}")

    for pkg_name, vers, expected in test_subcases:
        # Make the query
        query = {"pkg_name": pkg_name, "vers_range": vers}
        resp = httpx.post(f"{BASE_URL}/internal/query_vers", json=query)

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
