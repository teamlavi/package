package pip

import (
	"dep-tree-gen/common"
	"dep-tree-gen/models"

	"dep-tree-gen/utils"
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
		id := utils.GenerateID(obj.Package.PackageName, obj.Package.InstalledVersion, common.PIP_REPO_NAME)
		if utils.Contains(pkgs, obj.Package.PackageName) {
			topLvlDependencyIds = append(topLvlDependencyIds, id)
		}
		dependencyIds := []string{}
		for _, dep := range obj.Dependencies {
			dependencyIds = append(dependencyIds, utils.GenerateID(dep.PackageName, dep.InstalledVersion, common.PIP_REPO_NAME))
		}
		nodes[id] = models.CDSNode{
			ID:           id,
			Package:      obj.Package.PackageName,
			Version:      obj.Package.InstalledVersion,
			Dependencies: dependencyIds,
		}
	}

	output := models.CDS{
		CmdType:    common.PIP_CMD_NAME,
		Repository: common.PIP_REPO_NAME,
		Nodes:      nodes,
		Root: models.CDSNode{
			Dependencies: topLvlDependencyIds,
		},
	}

	return output
}
