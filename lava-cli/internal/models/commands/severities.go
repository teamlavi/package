package commands

import (
	"dep-tree-gen/utils"
	"fmt"
)

type SeveritiesResponse struct {
	SevList map[string][]string `json:"sevList"` // Vulnerable package id -> CVE Serverity type
}

func (a SeveritiesResponse) Display() {
	for k, v := range a.SevList {
		name, version, _ := utils.DecodeID(k)
		fmt.Printf("CVE Severities found in %s==%s: %v\n", name, version, v)
	}
}

func (a SeveritiesResponse) ToCSV() [][]string {
	out := [][]string{
		{"name", "version", "severities"},
	}
	for k, v := range a.SevList {
		name, version, _ := utils.DecodeID(k)
		out = append(out, []string{name, version, fmt.Sprintf("%v", v)})
	}

	return out
}
