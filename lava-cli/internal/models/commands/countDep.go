package commands

import (
	"dep-tree-gen/utils"
	"fmt"
)

type CountDepResponse struct {
	DepList map[string]int `json:"depList"` // package id -> Number of dependencies for this package
}

func (a CountDepResponse) Display() {
	for k, v := range a.DepList {
		name, version, _ := utils.DecodeID(k)
		fmt.Printf("%s==%s: %d\n", name, version, v)
	}
}

func (a CountDepResponse) ToCSV() [][]string {
	return [][]string{}
}
