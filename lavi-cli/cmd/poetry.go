/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package cmd

import (
	"encoding/json"
	"io/ioutil"

	"dep-tree-gen/generator"

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
		write, _ := cmd.Flags().GetBool("write")

		poetryGen := generator.GetPoetryTreeGenerator(path)
		cds := poetryGen.GetCDS()
		if write {
			file, _ := json.MarshalIndent(cds, "", " ")
			_ = ioutil.WriteFile("cds.json", file, 0644)
		}
	},
}

func init() {
	rootCmd.AddCommand(poetryCmd)
	poetryCmd.Flags().String("path", ".", "Path to project")
}
