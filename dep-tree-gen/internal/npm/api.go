package npm

import (
	"dep-tree-gen/models"
	"fmt"
	"log"
	"os"
	"path/filepath"
)

type NpmTreeGenerator struct {
	Path string
}

func (g NpmTreeGenerator) GetCDS() models.CDS {
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
