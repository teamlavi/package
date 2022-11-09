package vulnerabilities

import "dep-tree-gen/models"

func Scan(cds models.CDS) map[string]Vulnerability {

	pkgIds := []string{}
	for id, _ := range cds.Nodes {
		pkgIds = append(pkgIds, id)
	}

	// send request with pkg ids and convert

	return map[string]Vulnerability{}
}
