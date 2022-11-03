package poetry

import (
	"dep-tree-gen/internal/utils"
	"dep-tree-gen/models"
	"strings"
)

type LockFile struct {
	Package []Package
}

type Package struct {
	Name         string
	Version      string
	Dependencies map[string]string
}

type Pyproject struct {
	Tool struct {
		Poetry struct {
			Dependencies map[string]string
		}
	}
}

func poetryLockFileToCds(lockFile LockFile, pyproject Pyproject) models.CDS {

	nodes := map[string]models.CDSNode{}
	topLvlDependencyIds := []string{}

	filledVersionMap := map[string]string{}

	for _, obj := range lockFile.Package {
		filledVersionMap[obj.Name] = obj.Version
	}

	for _, obj := range lockFile.Package {
		id := utils.GenerateID(obj.Name, obj.Version, "poetry")
		dependencyIds := []string{}
		for depName, _ := range obj.Dependencies {
			dependencyIds = append(dependencyIds, utils.GenerateID(depName, filledVersionMap[depName], "poetry"))
		}
		nodes[id] = models.CDSNode{
			ID:           id,
			Package:      strings.ToLower(obj.Name),
			Version:      strings.ToLower(obj.Version),
			Dependencies: dependencyIds,
		}
	}

	for k, _ := range pyproject.Tool.Poetry.Dependencies {
		if k == "python" {
			continue
		}
		topLvlDependencyIds = append(topLvlDependencyIds, strings.ToLower(k))
	}

	output := models.CDS{
		Repository: "poetry",
		Nodes:      nodes,
		Root: models.CDSNode{
			Dependencies: topLvlDependencyIds,
		},
	}

	return output
}
