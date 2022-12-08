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

// vulnerablePackagesCmd represents the vulnerablePackages command
var vulnerablePackagesCmd = &cobra.Command{
	Use:   "vulnerablePackages",
	Short: "Return list of vulnerable packages",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			Api("analysis/vulnerable_packages").
			ResponseType(reflect.TypeOf(commands.VulPackagesResponse{})).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(vulnerablePackagesCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// vulnerablePackagesCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// vulnerablePackagesCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
