package models

import (
	"fmt"
	"log"
	"strings"

	"dep-tree-gen/utils"

	"github.com/spf13/cobra"
)

func getStringFlagValue(name string, cmd *cobra.Command, allowBlank bool) string {
	v, err := cmd.Flags().GetString(name)
	if err != nil {
		log.Fatalf("failed to read %s flag", name)
	}
	if v == "" && !allowBlank {
		log.Fatalf("%s flag must have a value provided", name)
	}
	return v
}

// checks for flag, and checks against repo whitelist
func getRepo(cmd *cobra.Command) Repo {
	v := getStringFlagValue("repo", cmd, false)
	return new(Repo).GetForValue(v)
}

func getLevel(cmd *cobra.Command) Level {
	level := getStringFlagValue("level", cmd, true)
	return new(Level).GetForValue(level)
}

func getStatus(cmd *cobra.Command) Status {
	val := getStringFlagValue("status", cmd, true)
	return new(Status).GetForValue(val)
}

func getPackages(cmd *cobra.Command) []string {
	v, err := cmd.Flags().GetStringSlice("packages")
	if err != nil {
		log.Fatal("failed to read packages flag")
	}

	out := []string{}
	for _, pkg := range v {
		if !strings.Contains(pkg, "==") {
			panic(fmt.Sprintf("Package %s is invalid. Format must be PACKAGE_NAME==PACKAGE_VERSION", pkg))
		}
		nameVers := strings.Split(pkg, "==")
		out = append(out, utils.GenerateID(nameVers[0], nameVers[1], string(getRepo(cmd))))
	}

	return out
}

func BuildLavaRequest(cmd *cobra.Command, requires ...Requires) (*LavaRequest, error) {
	lr := &LavaRequest{
		Repo:     getRepo(cmd),
		Status:   getStatus(cmd),
		Level:    getLevel(cmd),
		Packages: getPackages(cmd),
	}

	for _, r := range requires {
		ok, err := r(lr)
		if !ok {
			return nil, err
		}
	}

	return lr, nil

}
