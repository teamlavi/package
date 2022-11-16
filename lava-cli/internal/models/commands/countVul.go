package commands

type CountVulResponse struct {
	VulCount int `json:"vulCount"` // Total number of Vulns found in the packages in our database
}

func (a CountVulResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a CountVulResponse) Finalize() {
	panic("not implemented") // TODO: Implement
}
