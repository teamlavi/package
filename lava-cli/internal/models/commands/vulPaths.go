package commands

import (
	"dep-tree-gen/utils"
	"fmt"
)

type VulPathResponse struct {
	VulPath map[string]map[string][][]string `json:"vulPath"` // Package id -> Vulnerable Package id -> List of path lists
}

func (a VulPathResponse) Display() {
	for packageId, vulPackageData := range a.VulPath {
		name, version, _ := utils.DecodeID(packageId)
		fmt.Printf("Package: %s==%s\n", name, version)
		for vulPackageId, pathList := range vulPackageData {
			vulName, vulVersion, _ := utils.DecodeID(vulPackageId)
			fmt.Printf("\tVulnerable Package: %s==%s\n", vulName, vulVersion)
			for _, path := range pathList {
				fmt.Printf("\t\t%v", path)
			}
		}
	}
}

func (a VulPathResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "version", "vulnerable_dep_name", "vulnerable_dep_version", "path"},
	}
	for packageId, vulPackageData := range a.VulPath {
		name, version, _ := utils.DecodeID(packageId)
		for vulPackageId, pathList := range vulPackageData {
			vulName, vulVersion, _ := utils.DecodeID(vulPackageId)
			for _, path := range pathList {
				out = append(out, []string{name, version, vulName, vulVersion, fmt.Sprintf("%v", path)})
			}
		}
	}
	return out
}
