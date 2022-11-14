/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"dep-tree-gen/generator"

	"github.com/spf13/cobra"
)

// poetryCmd represents the poetry command
var poetryCmd = &cobra.Command{
	Use:   "poetry",
	Short: "Run LAVI against a python project (using poetry)",

	Run: func(cmd *cobra.Command, args []string) {
		path, _ := cmd.Flags().GetString("path")

		poetryGen := generator.GetPoetryTreeGenerator(path)
		cds := getCds(cmd, poetryGen)
		postCommand(cmd, cds, poetryGen)
	},
}

func init() {
	rootCmd.AddCommand(poetryCmd)
	poetryCmd.Flags().String("path", ".", "Path to project")
}
