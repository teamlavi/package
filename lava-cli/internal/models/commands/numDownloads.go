package commands

import (
	"dep-tree-gen/utils"
	"fmt"
	"strconv"
)

type NumDownloadsResponse struct {
	Downloads map[string]int `json:"downloads"` // Package id -> Number of package downloads
}

func (a NumDownloadsResponse) Display() {
	for pkg, count := range a.Downloads {
		fmt.Printf("Package %s: %d downloads\n", IdToString(pkg), count)
	}
}

func (a NumDownloadsResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "version", "count"},
	}
	for pkg, count := range a.Downloads {
		name, version, _ := utils.DecodeID(pkg)
		out = append(out, []string{name, version, strconv.Itoa(count)})
	}
	return out
}
