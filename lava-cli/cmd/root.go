/*
Copyright © 2022 LAVI Product Owners (James Purtilo and Guido Ambasz)
and the LAVI Development Team (Levi Lutz, Preetham Rudraraju, Paul Kolbeck, Tucker Siegel, John Perret, Quan Yuan, and Edson Cortes Rivera)
*/
package cmd

import (
	"github.com/spf13/cobra"
)

var cfgFile string

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "lava",
	Short: "Language Agnostic Vulnerability Analysis",
	Long:  `Each command may have different options. Be sure to use "lava [command] --help to see what options are available before running.`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	// Run: func(cmd *cobra.Command, args []string) { },
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	cobra.CheckErr(rootCmd.Execute())
}

func init() {
	rootCmd.PersistentFlags().String("api-key", "", "Lava backend api key")
	rootCmd.PersistentFlags().StringP("repo", "r", "", "Repo to run analysis on")
	// rootCmd.PersistentFlags().String("status", "", "Vulnerability status to look at (active, patched, or all)")
	// rootCmd.PersistentFlags().String("level", "", "Vulnerability depth levels to look at (direct, indirect, or all)")
	rootCmd.PersistentFlags().StringSlice("packages", []string{}, "Packages to look at")
	rootCmd.PersistentFlags().String("csv", "lava-response.csv", "Save to csv file")
	rootCmd.PersistentFlags().String("remote", "http://vocation.cs.umd.edu/api", "Remote api url. Must start with http:// or https://, and not end with a slash")
}
