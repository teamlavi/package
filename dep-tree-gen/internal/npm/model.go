package npm

import (
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"dep-tree-gen/utils"
	"strings"
)

type PackageLock struct {
	Name            string                `json:"name"`
	Version         string                `json:"version"`
	LockfileVersion int                   `json:"lockfileVersion"`
	Requires        bool                  `json:"requires"`
	Dependencies    map[string]Dependency `json:"dependencies"`
	// Packages        map[string]struct {
	// 	Name         string            `json:"name"`
	// 	Version      string            `json:"version"`
	// 	Dependencies map[string]string `json:"dependencies`
	// } `json:"packages"`
}

type Package struct {
	Name         string                 `json:"name"`
	Dependencies map[string]interface{} `json:"dependencies"`
}

type Dependency struct {
	Version      string                `json:"version"`
	Requires     map[string]string     `json:"requires"`
	Dependencies map[string]Dependency `json:"dependencies"`
	Peer         bool                  `json:"peer"`
}

type DepNode struct {
	name     string
	version  string
	requires []string
	peer     bool
}

func keys(data map[string]string) []string {
	out := []string{}
	for k, _ := range data {
		out = append(out, k)
	}
	return out
}

// flatten everything out into a map of the dependency path to dependency node
func (l PackageLock) flatten() map[string]*DepNode {
	depMap := map[string]*DepNode{}

	var flattenLockFileReq func(deps map[string]Dependency, path []string)

	flattenLockFileReq = func(deps map[string]Dependency, path []string) {
		for dName, dVal := range deps {
			if dVal.Version == "file:" || dVal.Peer {
				continue
			}
			item := &DepNode{
				name:     dName,
				version:  dVal.Version,
				requires: []string{},
			}

			if len(dVal.Requires) != 0 {
				item.requires = keys(dVal.Requires)
			}

			newPath := append(path, dName)
			key := strings.Join(newPath, "|")
			depMap[key] = item
			if len(dVal.Dependencies) != 0 {
				flattenLockFileReq(dVal.Dependencies, newPath)
			}
		}
	}

	flattenLockFileReq(l.Dependencies, []string{})
	return depMap
}

// this tells us which dependency requires another
func findDepsPath(startPath, depName string, depMap map[string]*DepNode) string {
	depPath := strings.Split(startPath, "|")
	for {
		currentPath := strings.Join(append(depPath, depName), "|")
		if _, exists := depMap[currentPath]; exists {
			return currentPath
		}
		if len(depPath) > 0 {
			depPath = depPath[:len(depPath)-1]
		} else {
			break
		}
	}
	return depName
}

func (lock PackageLock) ToCDS(pkgFile Package) models.CDS {
	depMap := lock.flatten()
	nodes := map[string]models.CDSNode{}
	pathToId := map[string]string{}
	for p, v := range depMap {
		id := utils.GenerateID(v.name, v.version, common.NPM_REPO_NAME)
		nodes[id] = models.CDSNode{
			ID:           id,
			Package:      v.name,
			Version:      v.version,
			Dependencies: []string{},
		}
		pathToId[p] = id
	}

	// set edges
	for path, dep := range depMap {
		pathObj := nodes[pathToId[path]]
		for _, dname := range dep.requires {
			subPath := findDepsPath(path, dname, depMap)
			pathId := pathToId[subPath]
			pathObj = models.CDSNode{
				ID:           pathObj.ID,
				Package:      pathObj.Package,
				Version:      pathObj.Version,
				Dependencies: append(pathObj.Dependencies, pathId),
			}
		}
		nodes[pathObj.ID] = pathObj
	}

	topLvlDependencyIds := []string{}
	for n, _ := range pkgFile.Dependencies {
		if id, exists := pathToId[n]; exists {
			topLvlDependencyIds = append(topLvlDependencyIds, id)
		}
	}

	output := models.CDS{
		CmdType:    common.NPM_CMD_NAME,
		Repository: common.NPM_REPO_NAME,
		Nodes:      nodes,
		Root: models.CDSNode{
			Dependencies: topLvlDependencyIds,
		},
	}

	return output
}
