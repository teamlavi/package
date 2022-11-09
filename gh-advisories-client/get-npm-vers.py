import json
import os

package = "react"

# might need this URL for downloads
# weekly downloads API url = 'https://api.npmjs.org/versions/'+package+'/last-week'

text = os.popen('npm show ' + package + '@* version --json').read()

version_list = json.loads(text)
for vers in version_list:
	major_vers, minor_vers, patch_vers = vers.split(".")
	print(major_vers, minor_vers, patch_vers)