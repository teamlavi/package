package commands

import (
	"dep-tree-gen/utils"
	"fmt"
	"strconv"
)

type TreeDepthsResponse struct {
	Depths map[string]int `json:"depths"` //  Breadth of each dependency tree in the input packages
}

func (a TreeDepthsResponse) Display() {
	for pkg, depth := range a.Depths {
		fmt.Printf("Package %s Dependency Tree Depth: %d\n", IdToString(pkg), depth)
	}
}

func (a TreeDepthsResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "version", "depth"},
	}
	for pkg, depth := range a.Depths {
		name, version, _ := utils.DecodeID(pkg)
		out = append(out, []string{name, version, strconv.Itoa(depth)})
	}
	return out
}
