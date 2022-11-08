package generator

import "dep-tree-gen/models"

type RepositoryTreeGenerator interface {
	GetCDS() models.CDS
	GetCDSForPackages(map[string]string) models.CDS
}
