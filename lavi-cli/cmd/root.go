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
	rootCmd.PersistentFlags().Bool("write-with-vulns", false, "When used with write, will include vulnerabilities in written tree")
	rootCmd.PersistentFlags().BoolP("show", "s", false, "Show ui")
	rootCmd.PersistentFlags().String("package", "", "Run lavi on a single package. If provided along with version, will default to running in single package mode")
	rootCmd.PersistentFlags().String("version", "", "Run lavi on a single package. If provided along with package, will default to running in single package mode")
	rootCmd.PersistentFlags().Bool("no-scan", false, "Ignore scanning the tree for vulnerabilities and only create the dependency tree")

	rootCmd.PersistentFlags().Bool("critical", false, "Only show critical severity vulnerabilities. Can be used alongside [--high, --medium, --low]")
	rootCmd.PersistentFlags().Bool("high", false, "Only show high severity vulnerabilities. Can be used alongside [--critical, --medium, --low]")
	rootCmd.PersistentFlags().Bool("medium", false, "Only show medium severity vulnerabilities. Can be used alongside [--critical, --high, --low]")
	rootCmd.PersistentFlags().Bool("low", false, "Only show low severity vulnerabilities. Can be used alongside [--critical, --high, --medium]")
}
