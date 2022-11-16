package commands

type SeveritiesResponse struct {
	SevList map[string]string `json:"sevList"` // Vulnerable package id -> CVE Serverity type
}

func (a SeveritiesResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a SeveritiesResponse) Finalize() {
	panic("not implemented") // TODO: Implement
}
