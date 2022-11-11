import httpx
import json

data = httpx.get("https://registry.npmjs.org/eslint-plugin-import/1.0.0").text
print(json.loads(data)['dependencies'])
