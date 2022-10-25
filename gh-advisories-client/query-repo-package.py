import requests
import json

repository = "PIP"
package = "numpy"

# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
token = ""

url = 'https://api.github.com/graphql'

query = """ {
securityVulnerabilities(first:100 ecosystem: """ + repository + """, package: \"""" + package + """\") {
    nodes {
      advisory {
        cwes(first:100){
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
}
"""

auth_headers = {"Authorization": "Bearer " + token}

r = requests.post(url, json={'query': query}, headers=auth_headers)
print(json.dumps(json.loads(r.text), indent=2))
