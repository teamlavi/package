import httpx
import json
import os

# TODO: include dev or other types of dependencies?

# cache completed trees
complete_trees = {}


def get_version(package: str, version_range: str):
    """Converts a version range to a singular version number (usually most recent release)"""
    if version_range[0] == "^" or version_range == "latest":
        return os.popen("npm view " + package + " version").read().strip()
    else:
        return version_range


def get_dependencies(package, version, tab=""):
    version = get_version(package, version)
    print(tab, package, version)

    if package + version in complete_trees:
        return complete_trees[package + version]

    data = httpx.get("https://registry.npmjs.org/" + package + "/" + version).text

    if "dependencies" not in json.loads(data).keys():
        complete_trees[package + version] = {}
        return {}

    dependency_dict = json.loads(data)["dependencies"]
    this_tree = {}
    for p in dependency_dict:
        v = get_version(p, dependency_dict.get(p))
        this_tree[p + v] = get_dependencies(p, v, tab + "\t")
    complete_trees[package + version] = this_tree
    # print(this_tree)
    return this_tree


# print(get_dependencies('react', '18.2.0'))

print(get_dependencies("request", "^1.0.0"))

print(complete_trees)
