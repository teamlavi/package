/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"dep-tree-gen/generator"

	"github.com/spf13/cobra"
)

// npmCmd represents the npm command
var npmCmd = &cobra.Command{
	Use:   "npm",
	Short: "Run LAVI against an npm project",
	Run: func(cmd *cobra.Command, args []string) {
		path, _ := cmd.Flags().GetString("path")
		npmGen := generator.GetNpmTreeGenerator(path)

		cds := getCds(cmd, npmGen)
		postCommand(cmd, cds, npmGen)
	},
}

func init() {
	rootCmd.AddCommand(npmCmd)
	npmCmd.Flags().String("path", ".", "Path to project")
}
