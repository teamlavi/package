/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "lavi",
	Short: "Language Agnostic Vulnerability Identifier",
	Long:  `LAVI is a tool built to help uncover hidden vulnerabilities that can be nested deeply inside a project's dependency tree.`,
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().BoolP("write", "w", false, "Write tree to a file")
	rootCmd.PersistentFlags().BoolP("show", "s", false, "Show ui")
	rootCmd.PersistentFlags().String("package", "", "Run lavi on a single package. If provided along with version, will default to running in single package mode")
	rootCmd.PersistentFlags().String("version", "", "Run lavi on a single package. If provided along with package, will default to running in single package mode")
}
