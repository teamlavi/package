import httpx
import json
import os

# TODO: include dev or other types of dependencies?

# cache completed trees
complete_trees = {}


def get_recent_vers(package):
    return os.popen("npm view " + package + " version").read().strip()


def get_dependencies(package, version, tab=""):
    if version[0] == "^":
        version = get_recent_vers(package)

    print(tab, package, version)

    if package + version in complete_trees:
        return complete_trees[package + version]

    data = httpx.get("https://registry.npmjs.org/" + package + "/" + version).text

    if "dependencies" not in json.loads(data).keys():
        complete_trees[package + version] = {}
        return {}

    dependency_list = json.loads(data)["dependencies"].keys()
    this_tree = {}
    for p in dependency_list:
        v = get_recent_vers(p)
        this_tree[p + v] = get_dependencies(p, v, tab + "\t")
    complete_trees[package + version] = this_tree
    # print(this_tree)
    return this_tree


# print(get_dependencies('react', '18.2.0'))

print(get_dependencies("gl-nodeutilities-test", "^1.0.0"))

print(complete_trees)
