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

// dependencyStatsCmd represents the dependencyStats command
var dependencyStatsCmd = &cobra.Command{
	Use:   "dependencyStats",
	Short: "Returns global dependency stats for the given repository",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			Api("analysis/dependency_stats").
			ResponseType(reflect.TypeOf(commands.DependencyStatsResponse{})).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(dependencyStatsCmd)
}
