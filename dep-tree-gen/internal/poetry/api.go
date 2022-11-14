package poetry

import (
	"dep-tree-gen/models"
	"log"
)

type PoetryTreeGenerator struct {
	Path string
}

func (g PoetryTreeGenerator) GetCDS() models.CDS {
	verifyPoetryDependency()
	lockFile := getPoetryLockFile(g.Path)
	pyproject := getPoetryTomlFileDependencues(g.Path)

	return lockFile.ToCDS(pyproject)
}

func (g PoetryTreeGenerator) GetCDSForPackages(pkgs map[string]string) models.CDS {
	return g.GetCDS()
}

func (g PoetryTreeGenerator) GenerateSinglePackageCds(pkg, version string) models.CDS {
	log.Fatal("unsupported")
	return models.CDS{}
}
