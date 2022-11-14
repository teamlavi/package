package cmd

import (
	"dep-tree-gen/models"
	"fmt"
	"lavi/internal/vulnerabilities"
	"os"
	"strings"

	"github.com/jedib0t/go-pretty/v6/table"
	"github.com/jedib0t/go-pretty/v6/text"
	"github.com/spf13/cobra"
)

func addSeverityColor(severity string) string {
	switch strings.ToLower(severity) {
	case "low":
		return text.FgHiGreen.Sprint("LOW")
	case "medium":
		return text.FgHiYellow.Sprint("MEDIUM")
	case "moderate":
		return text.FgHiYellow.Sprint("MEDIUM")
	case "high":
		return text.FgHiRed.Sprint("HIGH")
	case "critical":
		return text.FgHiRed.Sprint("CRITICAL")
	}
	return text.FgHiRed.Sprint(severity)
}

func mapOverVulns(vulns map[string][]vulnerabilities.VulnerabilityResponseData, f func(id string, v vulnerabilities.VulnerabilityResponseData)) {
	for id, vs := range vulns {
		for _, v := range vs {
			f(id, v)
		}
	}
}

func countVulns(vulns map[string][]vulnerabilities.VulnerabilityResponseData) int {
	foundCves := map[string]bool{}
	count := 0
	mapOverVulns(vulns, func(id string, v vulnerabilities.VulnerabilityResponseData) {
		if _, exists := foundCves[v.CVEID]; !exists {
			foundCves[v.CVEID] = true
			count += 1
		}
	})
	return count
}

func accumulateVulnCounts(vulns map[string][]vulnerabilities.VulnerabilityResponseData) []int {
	low := 0
	medium := 0
	high := 0
	critical := 0

	mapOverVulns(vulns, func(_ string, v vulnerabilities.VulnerabilityResponseData) {
		switch strings.ToLower(v.Severity) {
		case "low":
			low += 1
		case "medium":
			medium += 1
		case "moderate":
			medium += 1
		case "high":
			high += 1
		case "critical":
			critical += 1
		}
	})
	return []int{critical, high, medium, low}
}

func printCounts(vulns map[string][]vulnerabilities.VulnerabilityResponseData) {
	txt := []string{
		text.FgHiRed.Sprint("critical"),
		text.FgHiRed.Sprint("high"),
		text.FgHiYellow.Sprint("medium"),
		text.FgHiGreen.Sprint("low"),
	}
	hasPrinted := false
	for i, c := range accumulateVulnCounts(vulns) {
		plurality := "vulnerabilities"
		if c == 1 {
			plurality = "vulnerability"
		}
		if c != 0 && hasPrinted {
			fmt.Printf(", %d %s severity %s", c, txt[i], plurality)
		} else if c != 0 {
			fmt.Printf("%d %s severity %s", c, txt[i], plurality)
			hasPrinted = true
		}
	}
	fmt.Printf("\n")
}

func cmdHasAnyDisplayLimiters(cmd *cobra.Command) bool {
	low, _ := cmd.Flags().GetBool("low")
	medium, _ := cmd.Flags().GetBool("medium")
	high, _ := cmd.Flags().GetBool("high")
	critical, _ := cmd.Flags().GetBool("critical")
	return low || medium || high || critical
}

func display(cmd *cobra.Command, cds models.CDS, vulns map[string][]vulnerabilities.VulnerabilityResponseData) {
	fmt.Printf("Total dependencies checked: %d\n", len(cds.Nodes))

	count := countVulns(vulns)
	if count == 0 {
		fmt.Println("No vulnerabilities found!")
	} else {
		fmt.Printf("Found %d vulnerabilities\n", count)
	}

	printCounts(vulns)

	writers := map[string][]table.Writer{}

	mapOverVulns(vulns, func(id string, v vulnerabilities.VulnerabilityResponseData) {
		t := table.NewWriter()
		t.SetOutputMirror(os.Stdout)
		t.SetStyle(table.StyleLight)
		pkg := cds.Nodes[id]

		patchedIn := "-"
		if v.PatchedIn != "" {
			patchedIn = v.PatchedIn
		}

		t.AppendRow([]interface{}{addSeverityColor(v.Severity), v.Title})
		t.AppendSeparator()
		t.AppendRow([]interface{}{"Package", pkg.Package})
		t.AppendSeparator()
		t.AppendRow([]interface{}{"Version", pkg.Version})
		t.AppendSeparator()
		t.AppendRow([]interface{}{"Patched In", patchedIn})
		t.AppendSeparator()
		t.AppendRow([]interface{}{"Path", strings.Join(cds.GetPathString(id), " > ")})
		t.AppendSeparator()
		t.AppendRow([]interface{}{"Url", v.Url})

		if arr, exists := writers[v.Severity]; exists {
			arr = append(arr, t)
			writers[v.Severity] = arr
		} else {
			writers[v.Severity] = []table.Writer{t}
		}
	})

	mapFcn := func(name string, flagName string) {
		nameVal, _ := cmd.Flags().GetBool(flagName)
		if cmdHasAnyDisplayLimiters(cmd) && !nameVal {
			return
		}
		for _, w := range writers[name] {
			w.Render()
		}
	}

	mapFcn("CRITICAL", "critical")
	mapFcn("HIGH", "high")
	mapFcn("MEDIUM", "medium")
	mapFcn("MODERATE", "medium")
	mapFcn("LOW", "low")
}