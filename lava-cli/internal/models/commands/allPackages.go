package commands

import "fmt"

type AllPackagesResponse struct {
	Pkgs [][]string `json:"pkgs"`
}

func (a AllPackagesResponse) Display() {
	fmt.Printf("# Packages found: %d\n", len(a.Pkgs))
	fmt.Println("See the generated csv for full information")
}

func (a AllPackagesResponse) ToCSV() [][]string {
	out := [][]string{{
		"repo", "name", "version",
	}}
	for _, pkg := range a.Pkgs {
		out = append(out, pkg)
	}
	return out
}
