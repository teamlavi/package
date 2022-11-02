import requests
import json

"""
response = requests.get("https://api.npms.io/v2/search", params={"q":"not:unstable","size":"50"})
print(json.dumps(json.loads(response.text), indent=2))
"""

response = requests.get("https://registry.npmjs.org/react", headers={"Accept": "application/vnd.npm.install-v1+json" })
print(json.dumps(json.loads(response.text), indent=2))