package internal

import "dep-tree-gen/models"

type RepositoryTreeGenerator interface {
	GetCDS() models.CDS
}
