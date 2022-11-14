package npm

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"os/exec"
	"path/filepath"
)

func generatePackageLock(path string) {
	cmd := exec.Command("npm", "--prefix", path, "install", "--package-lock-only")
	err := cmd.Run()
	if err != nil {
		log.Fatal("failed to generate package-lock.json file")
	}
}

func parsePackageLock(path string) PackageLock {
	file, err := ioutil.ReadFile(filepath.Join(path, "package-lock.json"))
	if err != nil {
		log.Fatal("failed to read package-lock.json file")
	}
	var data PackageLock

	err = json.Unmarshal([]byte(file), &data)
	if err != nil {
		log.Fatal("unknown error occured during tree generation")
	}

	return data
}
