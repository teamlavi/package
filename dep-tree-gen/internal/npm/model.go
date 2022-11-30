package npm

import (
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"dep-tree-gen/utils"
	"fmt"
	"strings"
)

type PackageLock struct {
	Name            string                  `json:"name"`
	Version         string                  `json:"version"`
	LockfileVersion int                     `json:"lockfileVersion"`
	Requires        bool                    `json:"requires"`
	Dependencies    map[string]Dependency   `json:"dependencies"`
	Packages        map[string]DependencyV3 `json:"packages"`
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

type DependencyV3 struct {
	Version      string                 `json:"version"`
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

func keysInterface(data map[string]interface{}) []string {
	out := []string{}
	for k, _ := range data {
		out = append(out, k)
	}
	return out
}

// flatten everything out into a map of the dependency path to dependency node
func (l PackageLock) flatten() map[string]*DepNode {

	if l.LockfileVersion == 3 {
		return l.flattenV3()
	}

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

func (l PackageLock) FindDependencyV3InPackages(name string) (DependencyV3, error) {
	for n, d := range l.Packages {
		if strings.HasSuffix(n, name) {
			return d, nil
		}
	}
	return DependencyV3{}, fmt.Errorf("not found")
}

// lockfiles v3 are stupid and dont use the dependencies part anymore
func (l PackageLock) flattenV3() map[string]*DepNode {
	depMap := map[string]*DepNode{}
	rootDeps := l.Packages[""].Dependencies

	var flattenLockFileReq func(deps []string, path []string)

	flattenLockFileReq = func(deps []string, path []string) {
		for _, dName := range deps {

			dVal, err := l.FindDependencyV3InPackages(dName)
			if err != nil {
				continue
			}

			if dVal.Version == "file:" {
				continue
			}
			item := &DepNode{
				name:     dName,
				version:  dVal.Version,
				requires: []string{},
			}

			if len(dVal.Dependencies) != 0 {
				item.requires = keysInterface(dVal.Dependencies)
			}

			newPath := append(path, dName)
			key := strings.Join(newPath, "|")
			depMap[key] = item
			if len(dVal.Dependencies) != 0 {
				flattenLockFileReq(item.requires, newPath)
			}
		}
	}

	queue := []string{}

	for r, _ := range rootDeps {
		queue = append(queue, r)
	}

	flattenLockFileReq(queue, []string{})
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
