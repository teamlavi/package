package poetry

import (
	"dep-tree-gen/common"
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

func (lockFile LockFile) ToCDS(pyproject Pyproject) models.CDS {

	nodes := map[string]models.CDSNode{}
	topLvlDependencyIds := []string{}

	filledVersionMap := map[string]string{}

	for _, obj := range lockFile.Package {
		filledVersionMap[obj.Name] = obj.Version
	}

	for _, obj := range lockFile.Package {
		id := utils.GenerateID(obj.Name, obj.Version, common.POETRY_REPO_NAME)
		dependencyIds := []string{}
		for depName, _ := range obj.Dependencies {
			dependencyIds = append(dependencyIds, utils.GenerateID(depName, filledVersionMap[depName], common.POETRY_REPO_NAME))
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
		topLvlDependencyIds = append(topLvlDependencyIds, utils.GenerateID(k, filledVersionMap[strings.ToLower(k)], common.POETRY_REPO_NAME))
	}

	output := models.CDS{
		CmdType:    common.POETRY_CMD_NAME,
		Repository: common.POETRY_REPO_NAME,
		Nodes:      nodes,
		Root: models.CDSNode{
			Dependencies: topLvlDependencyIds,
		},
	}

	return output
}
