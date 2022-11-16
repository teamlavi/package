package commands

import "fmt"

type CountResponse struct {
	Count int `json:"count"` // Total number of packages in LAVI database
}

func (a CountResponse) Display() {
	fmt.Printf("Total Package Count: %d\n", a.Count)
}

func (a CountResponse) ToCSV() [][]string {
	return [][]string{}
}
