# too lazy to figure how to do this in bash
import subprocess
import os 
import shutil


wd = os.getcwd()
ui_dir = os.path.join(wd, "ui")

print ("installing ui dependencies")
subprocess.run(["npm", "install"], cwd=ui_dir)

print ("building ui")
subprocess.run(["npm", "run", "build"], cwd=ui_dir)

GOOS = ["darwin", "windows", "linux"]
GOARCHS = {
    "darwin": ["amd64", "arm64"],
    "windows": ["amd64", "arm"],
    "linux": ["amd64", "arm", "arm64"]
}

try:
    os.mkdir("archives")
except:
    pass

for goos in GOOS:
    for goarch in GOARCHS[goos]:
        env = os.environ.copy()
        env["GOOS"] = goos
        env["GOARCH"] = goarch

        name = f"lavi-cli-{goos}-{goarch}"

        print (f"building {name}")

        subprocess.run(["go", "build", "-o", "lavi"], env=env)
        os.mkdir(name)
        shutil.copy("INSTALL.txt", name)
        shutil.move("lavi", name)
        shutil.make_archive(f"archives/{name}", 'zip', name)
        shutil.rmtree(name)


