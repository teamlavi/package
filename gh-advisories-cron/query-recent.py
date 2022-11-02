import requests
import json

repository = "PIP"

# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
token = ""

last_cursor = "Y3Vyc29yOnYyOpK5MjAyMi0xMC0zMVQxODo0Mjo1OC0wNDowMM2LOA=="
url = 'https://api.github.com/graphql'

# TODO: Not sure if want to query securityAdvisories or securityVulnerabilities
# Edge gives cursor and node'
# Keep repository in query so that only relevant vulnerabilities are returned
query = """ 
{
  securityVulnerabilities(first:3, ecosystem: """ + repository + """, after: \"""" + last_cursor + """\") {
    edges {
      cursor
      node {
        advisory {
          cwes(first: 100) {
            nodes {
              cweId
            }
          }
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
        vulnerableVersionRange
      }
    }
    pageInfo {
      endCursor
    }
  }
}
"""

auth_headers = {"Authorization": "Bearer " + token}

r = requests.post(url, json={'query': query}, headers=auth_headers)
print(json.dumps(json.loads(r.text), indent=2))
