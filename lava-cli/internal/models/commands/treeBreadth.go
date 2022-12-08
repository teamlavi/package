package commands

import (
	"dep-tree-gen/utils"
	"fmt"
	"strconv"
)

type TreeBreadthsResponse struct {
	Breadths map[string]int `json:"breadths"` //  Breadth of each dependency tree in the input packages
}

func (a TreeBreadthsResponse) Display() {
	for pkg, breadth := range a.Breadths {
		fmt.Printf("Package %s Dependency Tree Breadth: %d\n", IdToString(pkg), breadth)
	}
}

func (a TreeBreadthsResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "version", "breadth"},
	}
	for pkg, breadth := range a.Breadths {
		name, version, _ := utils.DecodeID(pkg)
		out = append(out, []string{name, version, strconv.Itoa(breadth)})
	}
	return out
}
