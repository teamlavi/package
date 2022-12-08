/*
Copyright © 2022 LAVI Product Owners (James Purtilo and Guido Ambasz)
and the LAVI Development Team (Levi Lutz, Preetham Rudraraju, Paul Kolbeck, Tucker Siegel, John Perret, Quan Yuan, and Edson Cortes Rivera)
*/
package cmd

import (
	"lava/internal/client"
	"lava/internal/models/commands"
	"reflect"

	"github.com/spf13/cobra"
)

// allPackagesCmd represents the allPackages command
var allPackagesCmd = &cobra.Command{
	Use:   "allPackages",
	Short: "Returns all packages for which lava has a dependency tree",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			Api("analysis/all_packages").
			ResponseType(reflect.TypeOf(commands.AllPackagesResponse{})).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(allPackagesCmd)
}
