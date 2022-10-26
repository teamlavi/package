import requests
import json


repository = "PIP"

# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
token = ""

last_cursor = "Y3Vyc29yOnYyOpK5MjAyMi0xMC0wNlQxNjoxMDo0OC0wNDowMM2HsQ=="
url = 'https://api.github.com/graphql'

query = """ {
securityVulnerabilities(first:10, ecosystem: """ + repository + """, before: \"""" + last_cursor + """\") {
	pageInfo {
		startCursor
		endCursor
	}
	edges {
    cursor
    node {
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
}
"""

auth_headers = {"Authorization": "Bearer " + token}

r = requests.post(url, json={'query': query}, headers=auth_headers)
print(json.dumps(json.loads(r.text), indent=2))
