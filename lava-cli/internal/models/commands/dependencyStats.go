package commands

import (
	"fmt"
)

type DepStats struct {
	Mean   float64 `json:"mean"`
	Median float64 `json:"median"`
	Mode   float64 `json:"mode"`
	Stddev float64 `json:"stdDev"`
}

type DependencyStatsResponse struct {
	DepStats map[string]DepStats `json:"depStats"`
}

func (a DependencyStatsResponse) Display() {
	for repo, stats := range a.DepStats {
		fmt.Printf("Package Repository %s:\n", repo)
		fmt.Printf("\tMean Dependency Count: %f\n", stats.Mean)
		fmt.Printf("\tMedian Dependency Count: %f\n", stats.Median)
		fmt.Printf("\tMode Dependency Count: %f\n", stats.Mode)
		fmt.Printf("\tStandard Deviation of Dependency Counts: %f\n", stats.Stddev)
	}
}

func (a DependencyStatsResponse) ToCSV() [][]string {
	out := [][]string{
		{"repo", "mean_count", "median_count", "mode_count", "stddev_count"},
	}
	for repo, stats := range a.DepStats {
		out = append(out, []string{
			repo,
			fmt.Sprintf("%v", stats.Mean),
			fmt.Sprintf("%v", stats.Median),
			fmt.Sprintf("%v", stats.Mode),
			fmt.Sprintf("%v", stats.Stddev),
		})
	}
	return out
}
