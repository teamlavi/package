package commands

type CountDepResponse struct {
	DepList map[string]int `json:"depList"` // package id -> Number of dependencies for this package
}

func (a CountDepResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a CountDepResponse) Finalize() {
	panic("not implemented") // TODO: Implement
}
