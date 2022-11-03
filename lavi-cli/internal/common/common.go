package common

import (
	"dep-tree-gen/models"
	"encoding/json"
	"io/ioutil"
	"lavi-cli/internal/server"

	"github.com/spf13/cobra"
)

func PostCommand(cmd *cobra.Command, cds models.CDS) {
	write, _ := cmd.Flags().GetBool("write")
	show, _ := cmd.Flags().GetBool("show")
	if write {
		file, _ := json.MarshalIndent(cds, "", " ")
		_ = ioutil.WriteFile("cds.json", file, 0644)
	}

	if show {
		server.Serve()
	}
}
