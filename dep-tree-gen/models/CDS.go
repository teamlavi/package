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

func contains(val string, arr []string) bool {
	for _, a := range arr {
		if val == a {
			return true
		}
	}
	return false
}

func (c CDS) IsRoot(id string) bool {
	return contains(id, c.Root.Dependencies)
}

func (c CDS) GetPathString(id string) []string {
	if c.IsRoot(id) {
		return []string{c.Nodes[id].Package}
	}
	out := []string{}
	for _, n := range c.Nodes {
		if contains(id, n.Dependencies) {
			path := c.GetPathString(n.ID)
			out = append(path, c.Nodes[id].Package)
			return out
		}
	}
	return out
}
