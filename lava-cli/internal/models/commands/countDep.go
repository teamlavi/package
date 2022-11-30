package commands

import (
	"dep-tree-gen/utils"
	"fmt"
	"strconv"
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
	out := [][]string{
		{"name", "version", "count"},
	}
	for k, v := range a.DepList {
		name, version, _ := utils.DecodeID(k)
		out = append(out, []string{name, version, strconv.Itoa(v)})
	}

	return out
}
