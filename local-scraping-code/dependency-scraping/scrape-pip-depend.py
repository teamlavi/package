import httpx
import json

response = httpx.get("https://pypi.org/pypi/numpy/json")
print(json.dumps(json.loads(response.text), indent=2))
