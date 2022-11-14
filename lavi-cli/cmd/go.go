/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"dep-tree-gen/generator"

	"github.com/spf13/cobra"
)

// goCmd represents the go command
var goCmd = &cobra.Command{
	Use:   "go",
	Short: "Run LAVI against a go project",
	Run: func(cmd *cobra.Command, args []string) {
		path, _ := cmd.Flags().GetString("path")
		goGen := generator.GetGoTreeGenerator(path)

		cds := getCds(cmd, goGen)
		postCommand(cmd, cds, goGen)
	},
}

func init() {
	rootCmd.AddCommand(goCmd)
	goCmd.Flags().String("path", ".", "Path to project")
}
