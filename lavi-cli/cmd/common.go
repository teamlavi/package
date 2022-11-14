package cmd

import (
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"lavi/internal"
	internalModels "lavi/internal/models"
	"lavi/internal/vulnerabilities"

	"github.com/spf13/cobra"
)

func getCds(cmd *cobra.Command, gen generator.RepositoryTreeGenerator) models.CDS {
	var cds models.CDS
	if ok, singlePackageCds := tryExecuteSinglePackageMode(cmd, gen); ok {
		cds = singlePackageCds
	} else {
		cds = gen.GetCDS()
	}
	return cds
}

// post command function to run AFTER a command has succesfully run
func postCommand(cmd *cobra.Command, cds models.CDS, gen generator.RepositoryTreeGenerator) {
	pkg, version := getPackageAndVersion(cmd)
	singlePkg := false
	if pkg != "" && version != "" {
		singlePkg = true
	}
	write, _ := cmd.Flags().GetBool("write")
	show, _ := cmd.Flags().GetBool("show")
	noScan, _ := cmd.Flags().GetBool("no-scan")
	writeWithVulns, _ := cmd.Flags().GetBool("write-with-vulns")

	clean := map[string][]vulnerabilities.Vulnerability{}
	results := map[string][]vulnerabilities.VulnerabilityResponseData{}

	if !noScan {
		results = vulnerabilities.Scan(cds)
		clean = vulnerabilities.ConvertToCleanResponse(results)

		display(cmd, cds, results)
	}

	if write {
		var fileData []byte
		if writeWithVulns {
			fileData, _ = json.MarshalIndent(addVulnsToCds(cds, results), "", " ")
		} else {
			fileData, _ = json.MarshalIndent(cds, "", " ")
		}

		_ = ioutil.WriteFile("cds.json", fileData, 0644)
	}

	if show && !singlePkg {
		internal.Serve(cmd, cds, gen, clean)
	} else if show && singlePkg {
		fmt.Println("WARNING: Running lavi in single package mode will disable the ui")
	}
}

func getPackageAndVersion(cmd *cobra.Command) (string, string) {
	pkg, _ := cmd.Flags().GetString("package")
	version, _ := cmd.Flags().GetString("version")
	return pkg, version
}

// will run in single package mode if requirements are satisfied
// returns true if single package mode is executed, false otherwise
func tryExecuteSinglePackageMode(cmd *cobra.Command, gen generator.RepositoryTreeGenerator) (bool, models.CDS) {
	pkg, version := getPackageAndVersion(cmd)
	if pkg == "" || version == "" {
		return false, models.CDS{}
	}

	cds := gen.GenerateSinglePackageCds(pkg, version)

	return true, cds
}

// will return a copy
func addVulnsToCds(cds models.CDS, vulns map[string][]vulnerabilities.VulnerabilityResponseData) internalModels.ExpandedCDS {
	nodes := map[string]internalModels.ExpandedCDSNode{}
	for id, node := range cds.Nodes {
		vs := vulns[id]
		nodes[id] = internalModels.ExpandedCDSNode{
			ID:              id,
			Package:         node.Package,
			Version:         node.Version,
			Dependencies:    node.Dependencies,
			Vulnerabilities: vs,
		}
	}

	out := internalModels.ExpandedCDS{
		CmdType:    cds.CmdType,
		Repository: cds.Repository,
		Root:       cds.Root,
		Nodes:      nodes,
	}
	return out
}
