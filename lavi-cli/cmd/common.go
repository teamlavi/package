package cmd

import (
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
	"encoding/json"
	"io/ioutil"
	"lavi/internal"
	"lavi/internal/vulnerabilities"

	"github.com/spf13/cobra"
)

// post command function to run AFTER a command has succesfully run
func postCommand(cmd *cobra.Command, cds models.CDS, gen generator.RepositoryTreeGenerator) {
	write, _ := cmd.Flags().GetBool("write")
	show, _ := cmd.Flags().GetBool("show")

	results := vulnerabilities.Scan(cds)

	if write {
		file, _ := json.MarshalIndent(cds, "", " ")
		_ = ioutil.WriteFile("cds.json", file, 0644)
	}

	if show {
		clean := vulnerabilities.ConvertToCleanResponse(results)
		internal.Serve(cmd, cds, gen, clean)
	}
}
