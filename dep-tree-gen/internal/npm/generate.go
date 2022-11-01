package npm

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
)

func GenerateTree(path string) {
	if _, err := os.Stat(filepath.Join(path, "package.json")); err != nil {
		panic("project must contain package.json")
	}
	if _, err := os.Stat(filepath.Join(path, "package-lock.json")); err != nil {
		fmt.Println("No package-lock found. Generating...") // maybe include a seconds counter just so people know its doing stuff
		generatePackageLock(path)
	}

	packageLock := parsePackageLock(path)
	cds := packageLockToCds(packageLock)

	file, _ := json.MarshalIndent(cds, "", " ")
	_ = ioutil.WriteFile("test.json", file, 0644)
}

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
