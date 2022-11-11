import httpx
import json

# TODO: create list of fully searched trees to not search again
def get_dependencies(package, version, tab):
	if version[0] == "^":
		version = version[1:]
	print(tab, package, version)
	data = httpx.get("https://registry.npmjs.org/"+package+"/"+version).text
	if 'dependencies' in json.loads(data).keys():
		dependency_dict =  json.loads(data)['dependencies']
	elif 'devDependencies' in json.loads(data).keys():
		dependency_dict = json.loads(data)['devDependencies']
	else:
		# print(json.loads(data).keys())
		return
	for p in dependency_dict:
		get_dependencies(p, dependency_dict[p], tab+"\t")

get_dependencies('eslint-plugin-import', '1.0.0', '')
