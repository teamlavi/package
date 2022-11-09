package config

import (
	"dep-tree-gen/generator"
	"dep-tree-gen/models"

	"github.com/spf13/cobra"
)

type ConfigInterface interface {
	GetRepository() string
	GetCDS() models.CDS
	GetOriginalCDS() models.CDS
	SetCDS(models.CDS)
	SetOriginalCDS(models.CDS)
	GetGenerator() generator.RepositoryTreeGenerator
	GetCmd() *cobra.Command
}
