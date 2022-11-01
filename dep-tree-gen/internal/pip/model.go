package pip

import (
	"dep-tree-gen/models"
	"strings"

	"dep-tree-gen/internal/utils"
)

type PDPPackage struct {
	Key              string `json:"key"`
	PackageName      string `json:"package_name"`
	InstalledVersion string `json:"installed_version"`
}

type PDPObject struct {
	Package      PDPPackage   `json:"package"`
	Dependencies []PDPPackage `json:"dependencies"`
}

func pdpObjectArrToCds(arr []PDPObject, pkgs []string) models.CDS {

	nodes := map[string]models.CDSNode{}
	topLvlDependencyIds := []string{}

	for _, obj := range arr {
		id := utils.GenerateID(strings.ToLower(obj.Package.PackageName), strings.ToLower(obj.Package.InstalledVersion), "pip")
		if utils.Contains(pkgs, obj.Package.PackageName) {
			topLvlDependencyIds = append(topLvlDependencyIds, id)
		}
		dependencyIds := []string{}
		for _, dep := range obj.Dependencies {
			dependencyIds = append(dependencyIds, utils.GenerateID(strings.ToLower(dep.PackageName), strings.ToLower(dep.InstalledVersion), "pip"))
		}
		nodes[id] = models.CDSNode{
			ID:           id,
			Package:      obj.Package.PackageName,
			Version:      obj.Package.InstalledVersion,
			Dependencies: dependencyIds,
		}
	}

	output := models.CDS{
		Repository: "pip",
		Nodes:      nodes,
		Root: models.CDSNode{
			Dependencies: topLvlDependencyIds,
		},
	}

	return output
}
