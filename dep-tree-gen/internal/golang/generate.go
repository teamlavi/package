package golang

import (
	"bytes"
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"dep-tree-gen/utils"
	"log"
	"os/exec"
	"strings"
)

func generateTree(path string) string {
	cmd := exec.Command("go", "mod", "graph")
	cmd.Dir = path
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		log.Fatal("failed to call `go mod graph` for project")
	}
	return out.String()
}

func outputTreeToCds(name, tree string) models.CDS {

	nodes := map[string]models.CDSNode{}
	topLvlDependencyIds := []string{}

	for _, line := range strings.Split(tree, "\n") {
		if line == "" {
			continue
		}
		if strings.HasPrefix(line, name) {
			dep := strings.Split(strings.Split(line, " ")[1], "@")
			id := utils.GenerateID(dep[0], dep[1], common.GO_REPO_NAME)
			nodes[id] = models.CDSNode{
				ID:           id,
				Package:      dep[0],
				Version:      dep[1],
				Dependencies: []string{},
			}
			topLvlDependencyIds = append(topLvlDependencyIds, id)
		} else {
			deps := strings.Split(line, " ")
			dep1 := strings.Split(deps[0], "@")
			dep2 := strings.Split(deps[1], "@")

			dep1Id := utils.GenerateID(dep1[0], dep1[1], common.GO_REPO_NAME)
			dep2Id := utils.GenerateID(dep2[0], dep2[1], common.GO_REPO_NAME)

			dep1Node := nodes[dep1Id]
			dep1Node.Dependencies = append(dep1Node.Dependencies, dep2Id)
			nodes[dep1Id] = dep1Node

			nodes[dep2Id] = models.CDSNode{
				ID:           dep2Id,
				Package:      dep2[0],
				Version:      dep2[1],
				Dependencies: []string{},
			}
		}
	}

	output := models.CDS{
		CmdType:    common.GO_CMD_NAME,
		Repository: common.GO_REPO_NAME,
		Nodes:      nodes,
		Root: models.CDSNode{
			Dependencies: topLvlDependencyIds,
		},
	}

	return output
}
