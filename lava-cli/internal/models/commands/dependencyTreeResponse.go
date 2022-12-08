package commands

import (
	"dep-tree-gen/utils"
	"fmt"
)

type DependencyTreeResponse struct {
	DepTrees map[string]map[string][]string `json:"depTrees"`
}

func (a DependencyTreeResponse) Display() {
	fmt.Println("This command generates no display")
}

func (a DependencyTreeResponse) ToCSV() [][]string {
	out := [][]string{
		{"root_name", "root_version", "package", "version", "depends_on"},
	}
	for rootPkg, tree := range a.DepTrees {
		rootName, rootVersion, _ := utils.DecodeID(rootPkg)
		for pkg, dependsOn := range tree {
			pkgName, pkgVersion, _ := utils.DecodeID(pkg)
			dependsOnClean := IdArrayToStringArray(dependsOn)
			out = append(out, []string{rootName, rootVersion, pkgName, pkgVersion, AnyArrayToString(dependsOnClean)})
		}
	}
	return out
}
