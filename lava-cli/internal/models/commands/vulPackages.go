package commands

import "fmt"

type VulPackagesResponse struct {
	VulList []string `json:"vulList"` // List of all the package ids that are vulnerable in our database
}

func (a VulPackagesResponse) Display() {
	fmt.Printf("Vulnerable Packages Found: %v\n", a.VulList)
}

func (a VulPackagesResponse) ToCSV() [][]string {
	out := [][]string{
		{"package"},
	}
	for _, k := range a.VulList {
		out = append(out, []string{k})
	}
	return out
}
