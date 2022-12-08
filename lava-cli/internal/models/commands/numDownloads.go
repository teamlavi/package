package commands

import (
	"fmt"
)

type NumDownloadsResponse struct {
	Downloads map[string]string `json:"downloads"` // Package id -> Number of package downloads
}

func (a NumDownloadsResponse) Display() {
	for pkg, count := range a.Downloads {
		fmt.Printf("Package %s: %s downloads\n", pkg, count)
	}
}

func (a NumDownloadsResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "count"},
	}
	for pkg, count := range a.Downloads {
		out = append(out, []string{pkg, count})
	}
	return out
}
