package npm

import (
	"dep-tree-gen/models"

	"dep-tree-gen/internal/utils"
)

type PackageLock struct {
	Name            string                `json:"name"`
	Version         string                `json:"version"`
	LockfileVersion int                   `json:"lockfileVersion"`
	Requires        bool                  `json:"requires"`
	Dependencies    map[string]Dependency `json:"dependencies"`
	Packages        map[string]struct {
		Name         string            `json:"name"`
		Version      string            `json:"version"`
		Dependencies map[string]string `json:"dependencies`
	} `json:"packages"`
}

type Dependency struct {
	Version  string            `json:"version"`
	Requires map[string]string `json:"requires"`
}

func packageLockToCds(lock PackageLock) models.CDS {
	rootPkg := lock.Packages[""]

	nodes := map[string]models.CDSNode{}
	topLvlDependencyIds := []string{}

	for name, data := range lock.Dependencies {
		id := utils.GenerateID(name, data.Version, "npm")
		if _, exists := rootPkg.Dependencies[name]; exists {
			topLvlDependencyIds = append(topLvlDependencyIds, id)
		}

		dependencyIds := []string{}
		for depName, _ := range data.Requires {
			dependencyIds = append(dependencyIds, utils.GenerateID(depName, lock.Dependencies[depName].Version, "npm"))
		}
		nodes[id] = models.CDSNode{
			ID:           id,
			Package:      name,
			Version:      data.Version,
			Dependencies: dependencyIds,
		}
	}

	output := models.CDS{
		Repository: "npm",
		Nodes:      nodes,
		Root: models.CDSNode{
			Dependencies: topLvlDependencyIds,
		},
	}

	return output
}
