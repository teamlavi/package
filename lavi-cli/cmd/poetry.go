/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"dep-tree-gen/generator"
	"lavi/internal/common"

	"github.com/spf13/cobra"
)

// poetryCmd represents the poetry command
var poetryCmd = &cobra.Command{
	Use:   "poetry",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		path, _ := cmd.Flags().GetString("path")

		poetryGen := generator.GetPoetryTreeGenerator(path)
		cds := poetryGen.GetCDS()
		common.PostCommand(cmd, cds, poetryGen)
	},
}

func init() {
	rootCmd.AddCommand(poetryCmd)
	poetryCmd.Flags().String("path", ".", "Path to project")
}
