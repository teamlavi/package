package commands

import (
	"dep-tree-gen/utils"
	"fmt"
	"strconv"
)

type AffectedCountResponse struct {
	PkgsAffected map[string]int `json:"pkgsAffected"` // CVE id -> Number of packages affected
}

func (a AffectedCountResponse) Display() {
	fmt.Printf("Total Packages Affected: \n")
	for k, v := range a.PkgsAffected {
		name, version, _ := utils.DecodeID(k)
		fmt.Printf("Packages affected by vulnerabilities found in %s==%s: %v\n", name, version, v)
	}
}

func (a AffectedCountResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "version", "count"},
	}
	for k, v := range a.PkgsAffected {
		name, version, _ := utils.DecodeID(k)
		out = append(out, []string{name, version, strconv.Itoa(v)})
	}
	return out
}
