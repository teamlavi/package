package models

type CDS struct {
	// need this because pip and poetry are the same repo but different commands
	CmdType    string             `json:"cmdType"`
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
