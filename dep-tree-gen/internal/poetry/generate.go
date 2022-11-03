package poetry

import (
	"log"
	"os/exec"
	"path/filepath"

	"github.com/BurntSushi/toml"
)

func verifyPoetryDependency() {
	cmd := exec.Command("poetry")
	err := cmd.Run()
	if err != nil {
		log.Fatal("failed to find poetry on the system")
	}
}

func getPoetryLockFile(path string) LockFile {
	var lf LockFile
	_, err := toml.DecodeFile(filepath.Join(path, "poetry.lock"), &lf)
	if err != nil {
		log.Fatal("failed to parse poetry.lock")
	}

	return lf
}

func getPoetryTomlFileDependencues(path string) Pyproject {
	var lf Pyproject
	_, err := toml.DecodeFile(filepath.Join(path, "pyproject.toml"), &lf)
	if err != nil {
		log.Fatal("failed to parse pyproject.toml")
	}

	return lf
}
