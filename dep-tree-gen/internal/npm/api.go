package npm

import (
	"dep-tree-gen/models"
	"fmt"
	"os"
	"path/filepath"
)

type NpmTreeGenerator struct {
	Path string
}

func (g NpmTreeGenerator) GetCDS() models.CDS {
	if _, err := os.Stat(filepath.Join(g.Path, "package.json")); err != nil {
		panic("project must contain package.json")
	}
	if _, err := os.Stat(filepath.Join(g.Path, "package-lock.json")); err != nil {
		fmt.Println("No package-lock found. Generating...") // maybe include a seconds counter just so people know its doing stuff
		generatePackageLock(g.Path)
	}

	packageLock := parsePackageLock(g.Path)
	cds := packageLockToCds(packageLock)

	return cds
}
