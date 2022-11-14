package models

import (
	"dep-tree-gen/models"
	"lavi/internal/vulnerabilities"
)

type ExpandedCDSNode struct {
	ID              string                                      `json:"id,omitempty"`
	Package         string                                      `json:"package,omitempty"`
	Version         string                                      `json:"version,omitempty"`
	Dependencies    []string                                    `json:"dependencies"`
	Vulnerabilities []vulnerabilities.VulnerabilityResponseData `json:"vulnerabilities"`
}

type ExpandedCDS struct {
	CmdType    string                     `json:"cmdType"`
	Repository string                     `json:"repository"`
	Nodes      map[string]ExpandedCDSNode `json:"nodes"`
	Root       models.CDSNode             `json:"root"`
}
