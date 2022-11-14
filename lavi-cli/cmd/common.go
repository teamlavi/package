package cmd

import (
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"lavi/internal"
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

func display(cds models.CDS, vulns map[string][]vulnerabilities.Vulnerability) {
	fmt.Printf("package repository: %s\n", cds.Repository)
	fmt.Printf("total dependencies checked: %d\n", len(cds.Nodes))
	fmt.Println("this will show more eventually")
}

// post command function to run AFTER a command has succesfully run
func postCommand(cmd *cobra.Command, cds models.CDS, gen generator.RepositoryTreeGenerator) {
	write, _ := cmd.Flags().GetBool("write")
	show, _ := cmd.Flags().GetBool("show")

	results := vulnerabilities.Scan(cds)
	clean := vulnerabilities.ConvertToCleanResponse(results)

	display(cds, clean)

	if write {
		file, _ := json.MarshalIndent(cds, "", " ")
		_ = ioutil.WriteFile("cds.json", file, 0644)
	}

	if show {
		internal.Serve(cmd, cds, gen, clean)
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
