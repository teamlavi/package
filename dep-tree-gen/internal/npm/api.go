package npm

import (
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"fmt"
	"log"
	"os"
	"path/filepath"
)

type NpmTreeGenerator struct {
	Path string
}

func (g NpmTreeGenerator) BackupFiles() error {
	pkg := filepath.Join(g.Path, "package.json")
	pkgLock := filepath.Join(g.Path, "package-lock.json")
	if err := common.BackupToTemp(pkg); err != nil {
		return err
	}
	if err := common.BackupToTemp(pkgLock); err != nil {
		return err
	}
	return nil
}

func (g NpmTreeGenerator) RestoreFiles() error {
	pkg := filepath.Join(g.Path, "package.json")
	pkgLock := filepath.Join(g.Path, "package-lock.json")
	if err := common.RestoreFromTemp(pkg); err != nil {
		return err
	}
	if err := common.RestoreFromTemp(pkgLock); err != nil {
		return err
	}
	return nil
}

func (g NpmTreeGenerator) GetCDS() models.CDS {
	common.HasExecutableFailOut("npm")

	if _, err := os.Stat(filepath.Join(g.Path, "package.json")); err != nil {
		log.Fatal("project must contain a package.json file")
	}
	if _, err := os.Stat(filepath.Join(g.Path, "package-lock.json")); err != nil {
		fmt.Println("No package-lock found. Generating...") // maybe include a seconds counter just so people know its doing stuff
		generatePackageLock(g.Path)
	}

	return parsePackageLock(g.Path).ToCDS()
}

func (g NpmTreeGenerator) GetCDSForPackages(pkgs map[string]string) models.CDS {
	return g.GetCDS()
}

func (g NpmTreeGenerator) GenerateSinglePackageCds(pkg, version string) models.CDS {

	fileData := fmt.Sprintf(`
{
	"name": "lavi-empty",
	"version": "0.0.0",
	"dependencies": {
		"%s": "%s"
	}
}
		`, pkg, version)

	// try to backup old files if they exist
	backupPkgJson := common.BackupFile("package.json")
	backupPkgLockJson := common.BackupFile("package-lock.json")

	fileBytes := []byte(fileData)
	err := os.WriteFile("package.json", fileBytes, 0644)
	if err != nil {
		common.RestoreFile(backupPkgJson, "package.json")
		common.RestoreFile(backupPkgLockJson, "package-lock.json")
		log.Fatal("failed to write new package.json")
	}

	cds := g.GetCDS()

	// now we restore
	common.RestoreFile(backupPkgJson, "package.json")
	common.RestoreFile(backupPkgLockJson, "package-lock.json")
	return cds
}
