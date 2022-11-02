import requests
import json

repository = "PIP"

# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
token = ""

# Get vulnerabilities after:
last_cursor = "Y3Vyc29yOnYyOpK5MjAyMi0xMC0zMVQxODo0Mjo1OC0wNDowMM2LOA=="

# Keep repository in query so that only relevant vulnerabilities are returned
query = """ 
{
  securityVulnerabilities(first:10, ecosystem: """ + repository + """, after: \"""" + last_cursor + """\") {
    edges {
      cursor
      node {
        advisory {
          cwes(first: 100) {
            nodes {
              cweId
            }
          }
          summary
          permalink
          identifiers {
            value
            type
          }
        }
        package {
          name
          ecosystem
        }
        severity
        updatedAt
        vulnerableVersionRange
      }
    }
    pageInfo {
      endCursor
    }
  }
}
"""

# Add authorization token to headers
auth_headers = {"Authorization": "Bearer " + token}
response = requests.post("https://api.github.com/graphql", json={'query': query}, headers=auth_headers)

# Print returned JSON
print(json.dumps(json.loads(response.text), indent=2))

# Save for next query
last_cursor_received = json.loads(response.text)['data']['securityVulnerabilities']['pageInfo']['endCursor']

# Variables to help with spelling errors
CVE_ID = "cve_id"
severity = "severity"
description = "description"
CWES = "cwes"
url = "url"
repo = "repo_name"
package = "pkg_name"
vulnerableVersionRange = "vulnVersRange"

# Parse each vulnerability returned
parsed_vulnerabilities = []
for gh_vuln_edge in json.loads(response.text)['data']['securityVulnerabilities']['edges']:
	parsed_vuln = {}
	gh_vuln = gh_vuln_edge['node']
	cursor = gh_vuln_edge['cursor']  # not sure if needed

	parsed_vuln[CVE_ID] = next((item['value'] for item in gh_vuln['advisory']['identifiers'] if item['type'] == 'CVE'), None)
	if parsed_vuln[CVE_ID] is None:
		# No CVE, don't add to database
		continue
	parsed_vuln[severity] = gh_vuln['severity']
	parsed_vuln[description] = gh_vuln['advisory']['summary']
	parsed_vuln[CWES] = ",".join([cwe_node['cweId'] for cwe_node in gh_vuln['advisory']['cwes']['nodes']])
	parsed_vuln[url] = gh_vuln['advisory']['permalink']
	parsed_vuln[repo] = gh_vuln['package']['ecosystem']
	parsed_vuln[package] = gh_vuln['package']['name']
	parsed_vuln[vulnerableVersionRange] = gh_vuln['vulnerableVersionRange']

	parsed_vulnerabilities.append(parsed_vuln)

print(parsed_vulnerabilities)
