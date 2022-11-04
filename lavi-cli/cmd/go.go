/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"dep-tree-gen/generator"
	"lavi/internal/common"

	"github.com/spf13/cobra"
)

// goCmd represents the go command
var goCmd = &cobra.Command{
	Use:   "go",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		path, _ := cmd.Flags().GetString("path")
		goGen := generator.GetGoTreeGenerator(path)
		cds := goGen.GetCDS()
		common.PostCommand(cmd, cds)
	},
}

func init() {
	rootCmd.AddCommand(goCmd)
	goCmd.Flags().String("path", ".", "Path to project")
}
