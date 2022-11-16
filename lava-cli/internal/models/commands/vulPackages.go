package commands

type VulPackagesResponse struct {
	VulList []string `json:"vulList"` // List of all the package ids that are vulnerable in our database
}

func (a VulPackagesResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a VulPackagesResponse) Finalize() {
	panic("not implemented") // TODO: Implement
}
