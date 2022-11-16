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

// countCmd represents the count command
var countCmd = &cobra.Command{
	Use:   "count",
	Short: "Number of packages",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("count called")
		// to get repo flag
		// repo := common.GetRepo(cmd)
	},
}

func init() {
	rootCmd.AddCommand(countCmd)
	// we dont need any flags for this
}
