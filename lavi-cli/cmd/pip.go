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
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("pip called")
		path, _ := cmd.Flags().GetString("path")
		pythonPath, _ := cmd.Flags().GetString("python")
		generator.GeneratePipTree(path, pythonPath)
	},
}

func init() {
	rootCmd.AddCommand(pipCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// pipCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	pipCmd.Flags().StringP("python", "p", "python", "Path or alias to call python from")
	pipCmd.Flags().String("path", "requirements.txt", "Path to requirements.txt")
}
