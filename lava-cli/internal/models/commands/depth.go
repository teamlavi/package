package commands

type DepthResponse struct {
	VulDepth map[string]int `json:"vulDepth"` // CVE id -> Vulnerability depth from root package
}

func (a DepthResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a DepthResponse) Finalize() {
	panic("not implemented") // TODO: Implement
}
