package config

import (
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
)

type ConfigInterface interface {
	GetCDS() models.CDS
	SetCDS(models.CDS)
	SetOriginalCDS(models.CDS)
	GetGenerator() generator.RepositoryTreeGenerator
}
