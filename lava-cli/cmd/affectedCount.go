/*
Copyright © 2022 LAVI Product Owners (James Purtilo and Guido Ambasz)
and the LAVI Development Team (Levi Lutz, Preetham Rudraraju, Paul Kolbeck, Tucker Siegel, John Perret, Quan Yuan, and Edson Cortes Rivera)
*/
package cmd

import (
	"lava/internal/client"
	"lava/internal/models"
	"lava/internal/models/commands"
	"reflect"

	"github.com/spf13/cobra"
)

// affectedCountCmd represents the affectedCount command
var affectedCountCmd = &cobra.Command{
	Use:   "affectedCount",
	Short: "For vulnerabilities found in queried packages return a list with the number of of packages affected by each vulnerability",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			Api("analysis/affected_count").
			ResponseType(reflect.TypeOf(commands.AffectedCountResponse{})).
			Requires(models.REQUIRES_PKG_LIST).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(affectedCountCmd)
}
