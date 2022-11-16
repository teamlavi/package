package commands

import "fmt"

type CountVulResponse struct {
	VulCount int `json:"vulCount"` // Total number of Vulns found in the packages in our database
}

func (a CountVulResponse) Display() {
	fmt.Printf("Vulnerable Packages: %d\n", a.VulCount)
}

func (a CountVulResponse) ToCSV() [][]string {
	return [][]string{}
}
