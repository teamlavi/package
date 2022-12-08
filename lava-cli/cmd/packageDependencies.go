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

// packageDependenciesCmd represents the packageDependencies command
var packageDependenciesCmd = &cobra.Command{
	Use:   "packageDependencies",
	Short: "Returns the dependency tree for specified packages",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			Api("analysis/package_dependencies").
			ResponseType(reflect.TypeOf(commands.DependencyTreeResponse{})).
			Requires(models.REQUIRES_PKG_LIST).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(packageDependenciesCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// packageDependenciesCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// packageDependenciesCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
