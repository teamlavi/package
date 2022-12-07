package commands

type TreeBreadthsResponse struct {
	Breadths []int `json:"breadths"` //  Breadth of each dependency tree in the input packages
}

func (a TreeBreadthsResponse) Display() {
	panic("unimplemented")
}

func (a TreeBreadthsResponse) ToCSV() [][]string {
	panic("unimplemented")
}
