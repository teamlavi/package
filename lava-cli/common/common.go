package common

import (
	"fmt"
	"log"
	"strings"

	"github.com/spf13/cobra"
)

var REPO_WHITELIST = []string{
	"go",
	"pip",
	"npm",
}

func whitelistContains(repo string) bool {
	for _, r := range REPO_WHITELIST {
		if r == repo {
			return true
		}
	}
	return false
}

// checks for flag, and checks against repo whitelist
func GetRepo(cmd *cobra.Command) string {
	repo, err := cmd.Flags().GetString("repo")
	if err != nil {
		log.Fatal("failed to read repo flag")
	}
	if repo == "" {
		log.Fatal("repo flag must be provided")
	}
	repo = strings.ToLower(repo)
	if !whitelistContains(repo) {
		log.Fatal(fmt.Sprintf("package repository %s is unsupported", repo))
	}
	return repo
}
