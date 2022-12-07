/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package cmd

import (
	"github.com/spf13/cobra"
)

var cfgFile string

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "lava",
	Short: "Language Agnostic Vulnerability Analysis",
	Long:  `Each command may have different options. Be sure to use "lava [command] --help to see what options are available before running.`,
	// Uncomment the following line if your bare application
	// has an action associated with it:
	// Run: func(cmd *cobra.Command, args []string) { },
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	cobra.CheckErr(rootCmd.Execute())
}

func init() {
	rootCmd.PersistentFlags().String("api-key", "", "Lava backend api key")
	rootCmd.PersistentFlags().StringP("repo", "r", "", "Repo to run analysis on (pip, npm, or go)")
	rootCmd.PersistentFlags().String("status", "", "Vulnerability status to look at (active, patched, or all)")
	rootCmd.PersistentFlags().String("level", "", "Vulnerability depth levels to look at (direct, indirect, or all)")
	rootCmd.PersistentFlags().StringSlice("packages", []string{}, "Packages to look at")
	rootCmd.PersistentFlags().String("csv", "lava-response.csv", "Save to csv file")
	rootCmd.PersistentFlags().String("remote", "http://vocation.cs.umd.edu/api", "Remote api url. Must start with http:// or https://, and not end with a slash")
}
