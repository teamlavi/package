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
	"lava/internal/client"
	"lava/internal/models/commands"
	"reflect"

	"github.com/spf13/cobra"
)

// affectedByCveCmd represents the affectedByCve command
var affectedByCveCmd = &cobra.Command{
	Use:   "affectedByCve",
	Short: "Returns all packages affected by a cve",
	Run: func(cmd *cobra.Command, args []string) {
		client.
			New().
			Cmd(cmd).
			FillPkgsFromCve().
			Api("analysis/affected_by_cve").
			ResponseType(reflect.TypeOf(commands.AffectedByCveResponse{})).
			Run()
	},
}

func init() {
	rootCmd.AddCommand(affectedByCveCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// affectedByCveCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	affectedByCveCmd.Flags().StringSlice("cves", []string{}, "CVEs to look at")
}
