package commands

import (
	"dep-tree-gen/utils"
	"fmt"
)

type DepthResponse struct {
	VulDepth map[string]map[string][]int `json:"vulDepth"` // CVE id -> Vulnerability depth from root package
}

func (a DepthResponse) Display() {
	for k, v := range a.VulDepth {
		name, version, _ := utils.DecodeID(k)
		fmt.Printf("%s==%s: \n", name, version)
		for cveId, arr := range v {
			fmt.Printf("\tDepth of vulnerability %s: %v\n", cveId, arr)
		}
	}
}

func (a DepthResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "version", "cveId", "depths"},
	}
	for k, v := range a.VulDepth {
		name, version, _ := utils.DecodeID(k)
		for cveId, arr := range v {
			out = append(out, []string{name, version, cveId, fmt.Sprintf("%v", arr)})
		}
	}

	return out
}
