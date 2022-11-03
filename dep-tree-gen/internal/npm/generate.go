package npm

import (
	"encoding/json"
	"io/ioutil"
	"os/exec"
	"path/filepath"
)

func generatePackageLock(path string) {
	cmd := exec.Command("npm", "--prefix", path, "install", "--package-lock-only")
	err := cmd.Run()
	if err != nil {
		panic(err)
	}
}

func parsePackageLock(path string) PackageLock {
	file, err := ioutil.ReadFile(filepath.Join(path, "package-lock.json"))
	if err != nil {
		panic(err)
	}
	var data PackageLock

	err = json.Unmarshal([]byte(file), &data)
	if err != nil {
		panic(err)
	}

	return data
}
