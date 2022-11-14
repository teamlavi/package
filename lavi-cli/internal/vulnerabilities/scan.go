package vulnerabilities

import (
	"bytes"
	"dep-tree-gen/models"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/schollz/progressbar/v3"
)

func ScanSet(ids []string) BatchVulnerabilityResponse {
	values := map[string][]string{"ids": ids}
	json_data, err := json.Marshal(values)

	if err != nil {
		panic("failed to scan for vulnerabilities")
	}

	resp, err := http.Post("https://temp.lavi-lava.com/lavi/find_vulnerabilities_id_list", "application/json",
		bytes.NewBuffer(json_data))

	defer resp.Body.Close()

	if err != nil {
		panic("failed to scan for vulnerabilities")
	}
	var res BatchVulnerabilityResponse

	err = json.NewDecoder(resp.Body).Decode(&res)
	if err != nil {
		panic("failed to scan for vulnerabilities")
	}
	return res
}

func CleanupScanResults(all []BatchVulnerabilityResponse) map[string][]VulnerabilityResponseData {
	res := BatchVulnerabilityResponse{
		Vulns: map[string][]VulnerabilityResponseData{},
	}

	for _, item := range all {
		for k, v := range item.Vulns {
			if len(v) != 0 {
				res.Vulns[k] = v
			}
		}
	}

	return res.Vulns
}

func GrabSlice(start, end int, arr []string) ([]string, int) {
	if end > cap(arr) {
		return arr[start:], len(arr[start:])
	}
	return arr[start:end], len(arr[start:end])
}

func Scan(cds models.CDS) map[string][]VulnerabilityResponseData {
	pkgIds := []string{}
	for id, _ := range cds.Nodes {
		pkgIds = append(pkgIds, id)
	}
	fmt.Printf("Scanning %d packages for vulnerabilities\n", len(pkgIds))

	bar := progressbar.Default(int64(len(pkgIds)))
	all := []BatchVulnerabilityResponse{}

	// batch by groups of 100
	for i := 0; i < len(pkgIds); i += 100 {
		slice, count := GrabSlice(i, i+100, pkgIds)
		all = append(all, ScanSet(slice))
		bar.Add(count)
	}
	bar.Finish()

	return CleanupScanResults(all)
}

func severityToInt(sev string) int {
	switch v := strings.ToLower(sev); v {
	case "low":
		return 0
	case "medium":
		return 1
	case "moderate":
		return 1
	case "high":
		return 2
	case "critical":
		return 3
	}
	return 0
}

func ConvertToCleanResponse(data map[string][]VulnerabilityResponseData) map[string][]Vulnerability {
	out := map[string][]Vulnerability{}
	for k, v := range data {
		arr := []Vulnerability{}
		for _, vuln := range v {
			arr = append(arr, Vulnerability{
				CVEID:    vuln.CVEID,
				Url:      vuln.Url,
				Severity: severityToInt(vuln.Severity),
			})
		}
		out[k] = arr
	}
	return out
}

func Display(cds models.CDS, vulns map[string][]VulnerabilityResponseData) {
}
