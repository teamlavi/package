package poetry

import (
	"bufio"
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"errors"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
)

type PoetryTreeGenerator struct {
	Path string
}

func (g PoetryTreeGenerator) GetCDS() models.CDS {
	common.HasExecutableFailOut("poetry")
	lockFile := getPoetryLockFile(g.Path)
	pyproject := getPoetryTomlFileDependencues(g.Path)

	newLf := lockFile.CorrectSpecialCharacters()

	return newLf.ToCDS(pyproject)
}

func (g PoetryTreeGenerator) GetCDSForPackages(pkgs map[string]string) models.CDS {
	return g.GetCDS()
}

func (g PoetryTreeGenerator) GenerateSinglePackageCds(pkg, version string) models.CDS {
	common.HasExecutableFailOut("poetry")

	// generate a pyproject.toml WITHOUT dependencies installed
	// question: how do we reconcile existing python versions, and the 3.8 specified in this file
	fileData := `
[tool.poetry]
name = "lavi-temp"
version = "0.0.0"
description = ""
authors = ["LAVI CLI"]

[tool.poetry.dependencies]
python = "^3.10"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
`

	backupPyProject := common.BackupFile("pyproject.toml")
	backupPoetryLock := common.BackupFile("poetry.lock")

	fileBytes := []byte(fileData)
	err := os.WriteFile("pyproject.toml", fileBytes, 0644)
	if err != nil {
		log.Fatal("failed to write new pyproject.toml")
	}

	// need to trigger a lockfile only install of the package
	cmd := exec.Command("poetry", "add", "--lock", fmt.Sprintf("%s==%s", pkg, version))
	cmd.Stderr = cmd.Stdout
	stdout, _ := cmd.StdoutPipe()

	cmd.Start()

	reader := bufio.NewReader(stdout)
	line, err := reader.ReadString('\n')
	for err == nil {
		fmt.Print(line)
		line, err = reader.ReadString('\n')
	}
	if err != nil && !errors.Is(err, io.EOF) {
		log.Fatal("unknown error occured")
	}
	if err = cmd.Wait(); err != nil {
		common.RestoreFile(backupPyProject, "pyproject.toml")
		common.RestoreFile(backupPoetryLock, "poetry.lock")
		log.Fatal("Failed to create a lockfile for " + fmt.Sprintf("%s==%s", pkg, version) + ". Are you sure the package and version name combination is correct?")
	}

	// now we get the cds
	cds := g.GetCDS()

	// restore files if they exists
	common.RestoreFile(backupPyProject, "pyproject.toml")
	common.RestoreFile(backupPoetryLock, "poetry.lock")
	return cds
}
