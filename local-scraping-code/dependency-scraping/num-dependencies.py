import httpx
import json

data = httpx.get(
    "https://registry.npmjs.org/" + "no-one-left-behind" + "/" + "2018.2.10"
).text

# I think npm limits to 1000 dependencies?

print(len(json.loads(data)["dependencies"]))
