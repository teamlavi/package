package poetry

import (
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"dep-tree-gen/utils"
	"strings"

	"github.com/adrg/strutil"
	"github.com/adrg/strutil/metrics"
)

type LockFile struct {
	Package []Package
}

type Package struct {
	Name         string
	Version      string
	Dependencies map[string]interface{}
}

type Pyproject struct {
	Tool struct {
		Poetry struct {
			Dependencies map[string]interface{}
		}
	}
}

func contains(val string, arr []string) bool {
	for _, s := range arr {
		if s == val {
			return true
		}
	}
	return false
}

func mostSimilar(val string, arr []string) string {
	maxScore := -1000.0
	maxVal := ""
	for _, s := range arr {
		similarity := strutil.Similarity(val, s, metrics.NewLevenshtein())
		if similarity > maxScore {
			maxVal = s
			maxScore = similarity
		}
	}

	return maxVal
}

// creates a copy
func (lockFile LockFile) CorrectSpecialCharacters() LockFile {
	newPkgs := []Package{}
	names := []string{}
	for _, pkg := range lockFile.Package {
		names = append(names, pkg.Name)
	}

	for _, pkg := range lockFile.Package {
		newDeps := map[string]interface{}{}
		for d, _ := range pkg.Dependencies {
			name := d
			if !contains(d, names) {
				name = mostSimilar(d, names)
			}
			newDeps[name] = nil
		}
		newPkgs = append(newPkgs, Package{
			Name:         pkg.Name,
			Version:      pkg.Version,
			Dependencies: newDeps,
		})
	}

	return LockFile{
		Package: newPkgs,
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
