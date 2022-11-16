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
	"fmt"

	"github.com/spf13/cobra"
)

// severitiesCmd represents the severities command
var severitiesCmd = &cobra.Command{
	Use:   "severities",
	Short: "Return list of vulnerable packages and severity for each vulnerability",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("severities called")
	},
}

func init() {
	rootCmd.AddCommand(severitiesCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// severitiesCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// severitiesCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
