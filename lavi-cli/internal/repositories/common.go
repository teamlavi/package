package repositories

import "dep-tree-gen/models"

func CDSToPkgMap(cds models.CDS) map[string]string {
	pkgs := map[string]string{}
	for _, id := range cds.Root.Dependencies {
		node := cds.Nodes[id]
		pkgs[node.Package] = node.Version
	}
	return pkgs
}
