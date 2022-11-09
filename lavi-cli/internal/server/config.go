package server

import (
	"dep-tree-gen/generator"
	"dep-tree-gen/models"

	"github.com/spf13/cobra"
)

type ServerConfig struct {
	OriginalCDS models.CDS
	CDS         models.CDS
	Cmd         *cobra.Command
	Generator   generator.RepositoryTreeGenerator
}

func (s *ServerConfig) SetCDS(cds models.CDS) {
	s.CDS = cds
}

func (s *ServerConfig) SetOriginalCDS(cds models.CDS) {
	s.OriginalCDS = cds
}

func (s *ServerConfig) GetOriginalCDS() models.CDS {
	return s.OriginalCDS
}

func (s *ServerConfig) GetRepository() string {
	return s.OriginalCDS.Repository
}

func (s *ServerConfig) GetCDS() models.CDS {
	return s.CDS
}

func (s *ServerConfig) GetGenerator() generator.RepositoryTreeGenerator {
	return s.Generator
}

func (s *ServerConfig) GetCmd() *cobra.Command {
	return s.Cmd
}

// too lazy to add more error codes
var errorResp = map[string]string{
	"error": "internal server error occured",
}
