package commands

import (
	"dep-tree-gen/utils"
	"fmt"
)

type VulPackagesResponse struct {
	VulList []string `json:"vulList"` // List of all the package ids that are vulnerable in our database
}

func (a VulPackagesResponse) Display() {
	fmt.Printf("Total Vulnerable Package Count: %d\n", len(a.VulList))
}

func (a VulPackagesResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "version"},
	}
	for _, v := range a.VulList {
		name, version, _ := utils.DecodeID(v)
		out = append(out, []string{name, version})
	}
	return out
}
