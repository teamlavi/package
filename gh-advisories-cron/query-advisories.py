import requests
import json

repository = "PIP"


# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
token = ""

last_cursor = None

query_type = "securityAdvisories(last:100" \
			 + ("" if last_cursor is None or last_cursor == "" else ", after: \"" + last_cursor + "\"") \
			 + ", orderBy: {field: UPDATED_AT, direction: ASC})"

# Keep repository in query so that only relevant vulnerabilities are returned
query = """ 
{""" + query_type + """
   {
    edges {
      cursor
      
      node {
     identifiers{
     type
     value
     }
        vulnerabilities(first:100 ) {
        nodes{
        vulnerableVersionRange
        package {
          name
          ecosystem
        }
        }
      }
    }
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
# last_cursor_received = json.loads(response.text)['data']['securityVulnerabilities']['pageInfo']['endCursor']
