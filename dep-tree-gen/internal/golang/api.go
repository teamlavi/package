package golang

import (
	"dep-tree-gen/models"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

type GolangTreeGenerator struct {
	Path string
}

func (g GolangTreeGenerator) GetCDS() models.CDS {
	if _, err := os.Stat(filepath.Join(g.Path, "go.mod")); err != nil {
		panic("project must contain go.mod")
	}
	tree := generateTree(g.Path)
	modFile, err := ioutil.ReadFile(filepath.Join(g.Path, "go.mod"))
	if err != nil {
		panic(err)
	}

	name := strings.Split(strings.Split(string(modFile), "\n")[0], " ")[1]

	cds := outputTreeToCds(name, tree)
	return cds
}
