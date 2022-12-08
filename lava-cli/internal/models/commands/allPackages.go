package commands

import "fmt"

type AllPackagesResponse struct {
	Pkgs [][]string `json:"pkgs"`
}

func (a AllPackagesResponse) Display() {
	fmt.Printf("# Packages found: %d\n", len(a.Pkgs))
}

func (a AllPackagesResponse) ToCSV() [][]string {
	out := [][]string{{
		"repo", "name", "version",
	}}
	out = append(out, a.Pkgs...)
	return out
}
