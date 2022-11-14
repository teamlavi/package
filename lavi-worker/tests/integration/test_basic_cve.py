import functools

import httpx
import pytest

from .config import BASE_URL


TEST_VULN = {
    "cve_id": "CVE-1969-64209",
    "url": "https://github.com/advisories/GHSA-ab12-cd34-ef56",
    "repo_name": "pip",
    "pkg_name": "my-test-not-real-pkg",
    "pkg_vers": "1.2.3",
    "severity": "High",
    "description": "Buffer Overflow in the CLI",
}

TEST_VULN2 = {
    "cve_id": "CVE-1969-69209",
    "url": "https://github.com/advisories/GHSA-ab12-cd34-ef69",
    "repo_name": "pip",
    "pkg_name": "purtilos-sweatshop",
    "pkg_vers": "1.0.3",
    "severity": "High",
    "description": "Buffer Overflow in human sweat",
}

TEST_VULN3 = {
    "cve_id": "CVE-1969-69699",
    "url": "https://github.com/advisories/GHSA-ab12-cd34-ef69",
    "repo_name": "pip",
    "pkg_name": "purtilos-sweatshop",
    "pkg_vers": "1.4.3",
    "severity": "High",
    "description": "Buffer Overflow in human drippings",
}

TEST_VULN_VERS_CHECK = {
    "repo": TEST_VULN2["repo_name"],
    "package": TEST_VULN2["pkg_name"],
}

TEST_VULN_CHECK = {
    "repo": TEST_VULN["repo_name"],
    "package": TEST_VULN["pkg_name"],
    "version": TEST_VULN["pkg_vers"],
}


TEST_VULN_DELETE = {
    "repo_name": TEST_VULN["repo_name"],
    "pkg_name": TEST_VULN["pkg_name"],
    "pkg_vers": TEST_VULN["pkg_vers"],
    "cve_id": TEST_VULN["cve_id"],
}

TEST_VULN_DELETE2 = {
    "repo_name": TEST_VULN2["repo_name"],
    "pkg_name": TEST_VULN2["pkg_name"],
    "pkg_vers": TEST_VULN2["pkg_vers"],
    "cve_id": TEST_VULN2["cve_id"],
}

TEST_VULN_DELETE3 = {
    "repo_name": TEST_VULN3["repo_name"],
    "pkg_name": TEST_VULN3["pkg_name"],
    "pkg_vers": TEST_VULN3["pkg_vers"],
    "cve_id": TEST_VULN3["cve_id"],
}


def _assert_good_check_resp(resp):
    """Check a response from /find_vulnerabilities is ok, return vuln list."""
    resp.raise_for_status()
    parsed = resp.json()
    assert "vulns" in parsed
    return parsed["vulns"]


def _assert_fab_check_resp(resp):
    """Check a response from /find_vulnerabilities is ok, return vuln list."""
    resp.raise_for_status()
    parsed = resp.json()
    assert "vers" in parsed
    return parsed["vers"]


def _test_clean():
    """Clear up data left by tests.

    A little questionable to depend on a functioning endpoint pre-tests, but this allows
    us to run tests in live dev envs without messing other stuff up.
    """
    for req_body in [TEST_VULN_DELETE, TEST_VULN_DELETE2, TEST_VULN_DELETE3]:
        try:
            httpx.post(f"{BASE_URL}/internal/delete_vuln", json=req_body)
        except Exception:
            print("Failed to delete vuln pre-test (not critical)")
            pass  # don't let this be the failing point of tests


def _test_clean_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _test_clean()
        try:
            func(*args, **kwargs)
            _test_clean()
        except Exception as e:
            _test_clean()  # finally won't run if exc re-caught up stack
            raise e

    return wrapper


@_test_clean_decorator
def test_insert_check_cve():
    """Insert a vuln and check it applies to a package."""
    # Insert a vulnerability
    httpx.post(f"{BASE_URL}/internal/insert_vuln", json=TEST_VULN).raise_for_status()

    # Check if it affects the expeceted version
    resp = httpx.post(f"{BASE_URL}/find_vulnerabilities", json=TEST_VULN_CHECK)

    # Ensure it does affect it
    vulns = _assert_good_check_resp(resp)
    assert len(vulns) == 1 and vulns[0] == TEST_VULN["cve_id"]


@_test_clean_decorator
def test_double_insert_fails():
    """Test that you can't insert two of the same repo-pkg-vers-cve tuples."""
    # Insert a vulnerability (expected success)
    httpx.post(f"{BASE_URL}/internal/insert_vuln", json=TEST_VULN)

    # Insert the same one (expect failure)
    resp = httpx.post(f"{BASE_URL}/internal/insert_vuln", json=TEST_VULN)
    assert resp.text == "false"


@pytest.mark.parametrize(
    "transform_func",
    [
        lambda body: body.update({"repo": "npm"}),
        lambda body: body.update({"package": "my-other-not-real-pkg"}),
        lambda body: body.update({"version": "1.2.4"}),
    ],
)
@_test_clean_decorator
def test_no_sprawl(transform_func):
    """Test a CVE only affects declared repo/pkg/version."""
    # Insert a vulnerability
    httpx.post(f"{BASE_URL}/internal/insert_vuln", json=TEST_VULN).raise_for_status()

    # Check if it affects the expeceted version
    body = TEST_VULN_CHECK.copy()
    transform_func(body)
    resp = httpx.post(f"{BASE_URL}/find_vulnerabilities", json=body)

    # Ensure it does not affect it, but it should still 200
    vulns = _assert_good_check_resp(resp)
    assert len(vulns) == 0


@_test_clean_decorator
def test_vuln_versions():
    """Test a specific package."""
    # Insert a vulnerability
    httpx.post(f"{BASE_URL}/internal/insert_vuln", json=TEST_VULN).raise_for_status()
    httpx.post(f"{BASE_URL}/internal/insert_vuln", json=TEST_VULN2).raise_for_status()
    httpx.post(f"{BASE_URL}/internal/insert_vuln", json=TEST_VULN3).raise_for_status()

    # Check if it affects the expeceted version
    body = TEST_VULN_VERS_CHECK.copy()
    # transform_func(body)
    resp = httpx.post(f"{BASE_URL}/find_vulnerable_versions", json=body)

    # Ensure it does not affect it, but it should still 200
    vers = _assert_fab_check_resp(resp)
    assert len(vers) == 2
