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

// countDependenciesCmd represents the countDependencies command
var countDependenciesCmd = &cobra.Command{
	Use:   "countDependencies",
	Short: "Returns list of how many other packages each package relies on",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			Api("analysis/count_dependencies").
			ResponseType(reflect.TypeOf(commands.CountDepResponse{})).
			Requires(models.REQUIRES_PKG_LIST).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(countDependenciesCmd)
}
