package commands

type CountResponse struct {
	Count int `json:"count"` // Total number of packages in LAVI database
}

func (a CountResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a CountResponse) Finalize() {
	panic("not implemented") // TODO: Implement
}
