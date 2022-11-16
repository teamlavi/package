package commands

type TypesResponse struct {
	CweList map[string]int `json:"cweList"` // CWE id -> how many Vulnerabilities for this CWE
}

func (a TypesResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a TypesResponse) Finalize() {
	panic("not implemented") // TODO: Implement
}
