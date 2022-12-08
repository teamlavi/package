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

// numDownloadsCmd represents the numDownloads command
var numDownloadsCmd = &cobra.Command{
	Use:   "numDownloads",
	Short: "Get the number of downloads for the packages specified. Currently only works for pip",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			Api("analysis/num_downloads").
			ResponseType(reflect.TypeOf(commands.NumDownloadsResponse{})).
			Requires(models.REQUIRES_PKG_LIST).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(numDownloadsCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// numDownloadsCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// numDownloadsCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
