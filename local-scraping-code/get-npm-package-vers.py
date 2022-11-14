"""scrape_npm_packages() in updates.py"""

import json
import os

# install all-the-package-names
# os.system('npm i -g all-the-package-names')
# package_list = os.popen('all-the-package-names').read().split()

with open("npm-packages-w-vuln.txt", "r") as f:
    package_list = [p.replace("'", "") for p in f.read().split(", ")]

print("Starting scraping versions")
for package in package_list:
    if package[0] == "-":
        continue
    try:
        cmd = "npm view " + package + "@* version --json"
        # print(cmd)
        request = os.popen(cmd).read()
        # print(request)
        version_list = json.loads(request)

        if isinstance(version_list, str) and "-" in version_list:
            continue
        elif isinstance(version_list, str):
            version_list = [version_list]
        elif isinstance(version_list[0], list):
            version_list = version_list[0]
        for vers in version_list:
            major_vers, minor_vers, patch_vers = vers.split(".")
            # print(package, major_vers, minor_vers, patch_vers)
    except:
        print("unable to interpret versions for: ", package)
