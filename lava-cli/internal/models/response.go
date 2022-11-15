package models

type LavaResponse struct {
	Status string      `json:"status"`
	Error  interface{} `json:"error"`
	Result interface{} `json:"result"`
}

type AffectedCountResponse struct {
	PkgsAffected map[string]int `json:"pkgsAffected"` // CVE id -> Number of packages affected
}

type CountResponse struct {
	Count int `json:"count"` // Total number of packages in LAVI database
}

type CountDepResponse struct {
	DepList map[string]int `json:"depList"` // package id -> Number of dependencies for this package
}

type CountVulResponse struct {
	VulCount int `json:"vulCount"` // Total number of Vulns found in the packages in our database
}

type DepthResponse struct {
	VulDepth map[string]int `json:"vulDepth"` // CVE id -> Vulnerability depth from root package
}

type NumDownloadsResponse struct {
	Downloads map[string]int `json:"downloads"` // Package id -> Number of package downloads
}

type SeveritiesResponse struct {
	SevList map[string]string `json:"sevList"` // Vulnerable package id -> CVE Serverity type
}

type TypesResponse struct {
	CweList map[string]int `json:"cweList"` // CWE id -> how many Vulnerabilities for this CWE
}

type VulPackagesResponse struct {
	VulList []string `json:"vulList"` // List of all the package ids that are vulnerable in our database
}
