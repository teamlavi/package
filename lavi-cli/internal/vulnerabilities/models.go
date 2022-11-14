package vulnerabilities

type BatchVulnerabilityResponse struct {
	Vulns map[string][]VulnerabilityResponseData `json:"vulns"`
}

type VulnerabilityResponseData struct {
	CVEID    string `json:"cveId"`
	Severity string `json:"severity"`
	Url      string `json:"url"`
}

// this is how I want it for the ui - convert severity from high/moderate/low to int
type Vulnerability struct {
	CVEID    string `json:"cveId"`
	Severity int    `json:"severity"` // 0, 1, 2, 3 -> LOW, MEDIUM (or MODERATE), HIGH, CRITICAL
	Url      string `json:"url"`
}
