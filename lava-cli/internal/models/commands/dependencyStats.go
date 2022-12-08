package commands

import (
	"fmt"
)

type DependencyStatsResponse struct {
	Mean   float64 `json:"mean"`
	Median float64 `json:"median"`
	Mode   float64 `json:"mode"`
	Stddev float64 `json:"stdDev"`
}

func (a DependencyStatsResponse) Display() {
	fmt.Printf("Mean Dependency Count: %f\n", a.Mean)
	fmt.Printf("Median Dependency Count: %f\n", a.Median)
	fmt.Printf("Mode Dependency Count: %f\n", a.Mode)
	fmt.Printf("Standard Deviation of Dependency Counts: %f\n", a.Stddev)
}

func (a DependencyStatsResponse) ToCSV() [][]string {
	out := [][]string{
		{"mean_count", "median_count", "mode_count", "stddev_count"},
	}
	out = append(out, []string{
		fmt.Sprintf("%v", a.Mean),
		fmt.Sprintf("%v", a.Median),
		fmt.Sprintf("%v", a.Mode),
		fmt.Sprintf("%v", a.Stddev),
	})
	return out
}
