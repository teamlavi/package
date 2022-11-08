import httpx
import json

# GitHub personal access token (classic)
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
GitHub_access_token = ""


def scrape_vulns(repository="PIP"):
	auth_headers = {"Authorization": "Bearer " + GitHub_access_token}
	last_cursor_file = "lastCursor.txt"

	# Get and save cursor are functions incase decide to save somewhere else
	def get_last_cursor():
		try:
			with open(last_cursor_file, 'r+') as f:
				return f.read()
		except FileNotFoundError:
			return None


	def save_last_cursor(last_cursor):
		with open(last_cursor_file, 'w') as f:
			f.write(last_cursor)

	# Get vulnerabilities after:
	last_cursor = get_last_cursor()

	# Repeats until there are no new vulnerabilities
	while True:
		query_type = "securityVulnerabilities(first:100, ecosystem: " + repository \
				 + ("" if last_cursor is None or last_cursor == "" else ", after: \"" + last_cursor + "\"") \
				 + ", orderBy: {field: UPDATED_AT, direction: ASC})"

		# Keep repository in query so that only relevant vulnerabilities are returned
		query = """ 
		{""" + query_type + """
		   {
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
		response = httpx.post("https://api.github.com/graphql", json={'query': query}, headers=auth_headers)

		# Print returned JSON
		# print(json.dumps(json.loads(response.text), indent=2))

		# Save for next query
		last_cursor = json.loads(response.text)['data']['securityVulnerabilities']['pageInfo']['endCursor']

		if last_cursor is None:
			print("no newer vulns")
			return  # stop execution, no new data

		save_last_cursor(last_cursor)

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

		# Note: parsed_vulnerabilities might have duplicate CVE and packages with different affected version ranges
		# print(parsed_vulnerabilities) # Print parsed data
		# TODO insert parsed_vulnerabilities into DB

scrape_vulns("GO")