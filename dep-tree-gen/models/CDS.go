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

func (c CDS) FindRootParents(id string) []CDSNode {
	if c.IsRoot(id) {
		return []CDSNode{c.Nodes[id]}
	}

	out := []CDSNode{}
	for _, node := range c.Nodes {
		if contains(id, node.Dependencies) {
			out = append(out, c.FindRootParents(node.ID)...)
		}
	}
	return out
}
