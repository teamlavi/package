package golang

import (
	"dep-tree-gen/models"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
)

type GolangTreeGenerator struct {
	Path string
}

func (g GolangTreeGenerator) GetCDS() models.CDS {
	if _, err := os.Stat(filepath.Join(g.Path, "go.mod")); err != nil {
		log.Fatal("project must contain go.mod")
	}
	tree := generateTree(g.Path)
	modFile, err := ioutil.ReadFile(filepath.Join(g.Path, "go.mod"))
	if err != nil {
		log.Fatal("failed to read project go.mod file")
	}

	name := strings.Split(strings.Split(string(modFile), "\n")[0], " ")[1]

	cds := outputTreeToCds(name, tree)
	return cds
}

func (g GolangTreeGenerator) GetCDSForPackages(pkgs map[string]string) models.CDS {
	return g.GetCDS()
}

func (g GolangTreeGenerator) GenerateSinglePackageCds(pkg, version string) models.CDS {
	log.Fatal("unsupported")
	return models.CDS{}
}
