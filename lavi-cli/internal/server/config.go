package server

import (
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
	"lavi/internal/vulnerabilities"

	"github.com/spf13/cobra"
)

type ServerConfig struct {
	OriginalCDS                models.CDS
	CDS                        models.CDS
	CDSVulnerabilities         map[string][]vulnerabilities.Vulnerability
	OriginalCDSVulnerabilities map[string][]vulnerabilities.Vulnerability
	Cmd                        *cobra.Command
	Generator                  generator.RepositoryTreeGenerator
	Remote                     string
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

func (s *ServerConfig) GetVulns() map[string][]vulnerabilities.Vulnerability {
	return s.CDSVulnerabilities
}

func (s *ServerConfig) GetOriginalVulns() map[string][]vulnerabilities.Vulnerability {
	return s.OriginalCDSVulnerabilities
}

func (s *ServerConfig) SetVulns(d map[string][]vulnerabilities.Vulnerability) {
	s.CDSVulnerabilities = d
}

func (s *ServerConfig) GetRemote() string {
	return s.Remote
}

// too lazy to add more error codes
var errorResp = map[string]string{
	"error": "internal server error occured",
}
