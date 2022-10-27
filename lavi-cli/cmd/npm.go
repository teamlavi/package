/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"fmt"

	"dep-tree-gen/generator"

	"github.com/spf13/cobra"
)

// npmCmd represents the npm command
var npmCmd = &cobra.Command{
	Use:   "npm",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("slows down based on how big the tree is")
		path, _ := cmd.Flags().GetString("path")
		generator.GenerateNpmTree(path)
	},
}

func init() {
	rootCmd.AddCommand(npmCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// npmCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// npmCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
	npmCmd.Flags().String("path", ".", "Path to project")
}
