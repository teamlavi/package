package commands

import "fmt"

type VulPackagesResponse struct {
	VulList []string `json:"vulList"` // List of all the package ids that are vulnerable in our database
}

func (a VulPackagesResponse) Display() {
	fmt.Printf("Vulnerable Packages Found: %v\n", a.VulList)
	fmt.Printf("Count: %d\n", len(a.VulList))
}

func (a VulPackagesResponse) ToCSV() [][]string {
	out := [][]string{
		{"packages"},
	}
	for _, v := range a.VulList {
		out = append(out, []string{v})
	}
	return out
}
