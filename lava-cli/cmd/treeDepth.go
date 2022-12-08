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

// treeDepthCmd represents the treeDepth command
var treeDepthCmd = &cobra.Command{
	Use:   "treeDepth",
	Short: "Return the depth of the dependency tree",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			Api("analysis/tree_depth").
			ResponseType(reflect.TypeOf(commands.TreeDepthsResponse{})).
			Requires(models.REQUIRES_PKG_LIST).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(treeDepthCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// treeDepthCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// treeDepthCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
