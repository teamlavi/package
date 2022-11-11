import pytest

from lavi_worker.routers import external, internal, api_models
from lavi_worker.daos import cve


@pytest.mark.parametrize(
    "vulns",
    [
        (
            [
                cve.CVE(
                    id=0,
                    cve_id="A",
                    severity="High",
                    description="It makes ducks.",
                    cwe=None,
                    url="www.www.com",
                    repo_name="pip",
                    pkg_name="this-is-not-a-real-package",
                    pkg_vers="1.2.3",
                    univ_hash="this is a placeholder",
                ),
                cve.CVE(
                    id=1,
                    cve_id="B",
                    severity="Low",
                    description="Bananas Foster???",
                    cwe=None,
                    url="www.com.com",
                    repo_name="pip",
                    pkg_name="this-is-not-a-real-package-either",
                    pkg_vers="3.2.1",
                    univ_hash="this is definitely a placeholder",
                ),
                cve.CVE(
                    id=2,
                    cve_id="C",
                    severity=None,
                    description=None,
                    cwe=None,
                    url="www.www.com",
                    repo_name="pip",
                    pkg_name="this-is-not-a-real-package-again",
                    pkg_vers="2.0.2",
                    univ_hash="this is a placeholder too",
                ),
            ]
        )
    ],
)
async def test_find_vulnerabilities_id_list(vulns: list[cve.CVE]) -> None:
    # Insert vulnerability
    for vuln in vulns:
        internal.insert_vuln(
            api_models.InsertVulnRequest(
                cve_id=vuln.cve_id,
                url=vuln.url,
                repo_name=vuln.repo_name,
                pkg_name=vuln.pkg_name,
                pkg_vers=vuln.pkg_vers,
                severity=vuln.severity,
                description=vuln.description,
                cwe=vuln.cwe,
            )
        )
    try:
        # Check function output
        result = True
        vulnResponse = await external.find_vulnerabilities_id_list(
            api_models.FindVulnsIdListRequest(ids=[vuln.univ_hash for vuln in vulns])
        )
        rsp = vulnResponse.vulns
        for vuln in vulns:
            i = vuln.univ_hash
            if (
                rsp[i][0].cveId != vuln.cve_id
                or rsp[i][0].severity != vuln.severity
                or rsp[i][0].url != vuln.url
            ):
                result = False

    finally:
        # Delete vulnerabilities
        for vuln in vulns:
            internal.delete_vuln(
                api_models.DeleteVulnRequest(
                    repo_name=vuln.repo_name,
                    pkg_name=vuln.pkg_name,
                    pkg_vers=vuln.pkg_vers,
                    cve_id=vuln.cve_id,
                )
            )

    assert result
