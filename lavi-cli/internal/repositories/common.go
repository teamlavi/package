package repositories

import "dep-tree-gen/models"

func CDSToPkgMap(cds models.CDS) map[string]string {
	pkgs := map[string]string{}
	for _, node := range cds.Nodes {
		pkgs[node.Package] = node.Version
	}
	return pkgs
}
