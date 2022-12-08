package commands

import (
	"fmt"
	"strconv"
)

type AffectedByCveResponse struct {
	PkgsAffected map[string]int `json:"pkgsAffected"` // CVE id -> Number of packages affected
}

func (a AffectedByCveResponse) Display() {
	for k, v := range a.PkgsAffected {
		fmt.Printf("Packages affected by CVE %s: %v\n", k, v)
	}
	return
}

func (a AffectedByCveResponse) ToCSV() [][]string {
	out := [][]string{
		{"cveId", "count"},
	}
	for k, v := range a.PkgsAffected {
		out = append(out, []string{k, strconv.Itoa(v)})
	}
	return out

}
