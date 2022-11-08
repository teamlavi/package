package pip

import (
	"dep-tree-gen/models"
)

type PipTreeGenerator struct {
	// path is a path to requirements.txt
	Path string
	// PyPath can be either the alias to call python or the path to executable
	PythonPath string
}

func (g PipTreeGenerator) GetCDS() models.CDS {
	verifyPipDepTreeInstall(g.PythonPath)
	pkgs := getPackageNamesFromReq(g.Path)

	tree := callPDP(pkgs, g.PythonPath)
	cds := pdpObjectArrToCds(tree, pkgs)

	return cds
}

func (g PipTreeGenerator) GetCDSForPackages(pkgs map[string]string) models.CDS {
	data := []string{}
	for k, _ := range pkgs {
		data = append(data, k)
	}
	tree := callPDP(data, g.PythonPath)
	cds := pdpObjectArrToCds(tree, data)
	return cds
}
