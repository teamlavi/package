# too lazy to figure how to do this in bash
import subprocess
import os 

GOOS = "linux"
GOARCH = "amd64"

env = os.environ.copy()
env["GOOS"] = GOOS
env["GOARCH"] = GOARCH

subprocess.run(["go", "build", "-o", "lavi"], env=env)


