package models

type CDS struct {
	Repository string             `json:"repository"`
	Nodes      map[string]CDSNode `json:"nodes"`
	Root       CDSNode            `json:"root"`
}

type CDSNode struct {
	ID           string   `json:"id,omitempty"`
	Package      string   `json:"package,omitempty"`
	Version      string   `json:"version,omitempty"`
	Dependencies []string `json:"dependencies"`
}
