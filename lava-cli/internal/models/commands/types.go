package commands

import (
	"fmt"
	"strconv"
)

type TypesResponse struct {
	CweList map[string]int `json:"cweList"` // CWE id -> how many Vulnerabilities for this CWE
}

func (a TypesResponse) Display() {
	for k, v := range a.CweList {
		fmt.Printf("CWE: %s | Count: %d\n", k, v)
	}
}

func (a TypesResponse) ToCSV() [][]string {
	out := [][]string{
		{"cwe", "count"},
	}
	for k, v := range a.CweList {
		out = append(out, []string{k, strconv.Itoa(v)})
	}
	return out
}
