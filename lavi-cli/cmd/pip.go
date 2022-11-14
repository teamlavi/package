/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"fmt"

	"dep-tree-gen/generator"

	"github.com/spf13/cobra"
)

// pipCmd represents the pip command
var pipCmd = &cobra.Command{
	Use:   "pip",
	Short: "Run LAVI against a python project (using pip)",

	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("WARNING: This output may not be applicable to all systems. Please use a stronger dependency management system like poetry which includes a lockfile.")
		path, _ := cmd.Flags().GetString("path")
		pythonPath, _ := cmd.Flags().GetString("python")

		pipGen := generator.GetPipTreeGenerator(path, pythonPath)

		cds := getCds(cmd, pipGen)
		postCommand(cmd, cds, pipGen)
	},
}

func init() {
	rootCmd.AddCommand(pipCmd)
	pipCmd.Flags().StringP("python", "p", "python", "Path or alias to call python from")
	pipCmd.Flags().String("path", "requirements.txt", "Path to requirements.txt")
}
