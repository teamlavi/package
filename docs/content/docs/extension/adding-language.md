---
id: adding-language
title: Adding a Language
permalink: docs/extension/language.html
---

One of the principle design components of LAVI was to be extensible, so that any language can be added with relative ease. In order to do so, developers must know where to look to add that information.

Before extending LAVI, please make sure you understand how the backend works, and how [data](/docs/getting-started/data.html) is represented in the system.

## Backend

In order to add a new language to the backend, new components need to be added in a few places. 

### Scrapers

You must implement the following class, making it specific to your language

```python
# package/backend/scrapers/__init__.py
class RepoScraper(Protocol):
    @staticmethod
    def list_packages(partial: bool) -> list[str]:
        """Given this repository, return a list of its packages."""
        ...

    @staticmethod
    def list_package_versions(package: str, limit: int | None = None) -> list[str]:
        """Given this repository and package, return a list of available versions."""
        ...

    @staticmethod
    def generate_dependency_tree(package: str, version: str) -> TreeNode:
        """Given this repository, package, and version, return a conflict-free dep tree."""
        ...
```
And add the scraper to the `repo_scrapers` dict at the bottom of the file. And the `generate_dependency_tree` function relies on the LAVI cli supporting that language as well

## LAVI cli

### dep-tree-gen

Adding support for the new language in the LAVI cli starts in the `dep-tree-gen` package, where there is an interface called `RepositoryTreeGenerator`. This interface is intended to be the single way for golang clients to get a [CDS](/docs/getting-started/data.html#cds) for a given language.

```go
// package/dep-tree-gen/generator/api.go
type RepositoryTreeGenerator interface {
    // Get the CDS for the language
	GetCDS() models.CDS

	// allows for consistent calls in a single function - really on neccessary for pip
	// since thats the only repo that doesnt automatically update some dependency/lock file
	GetCDSForPackages(map[string]string) models.CDS

	// run single package generation mode
	GenerateSinglePackageCds(pkg, version string) models.CDS

    // backup any lock/dependency files
	BackupFiles() error

    // restore said lock/dependency files
	RestoreFiles() error
}
```
Once you implement the interface, you can add a function here to allow package users to get the implemented interface

```go
// package/dep-tree-gen/generator/generator.go

func Get(MY_NEW_REPOSITORY)TreeGenerator(path string) RepositoryTreeGenerator {
	return (REPO).(REPO)TreeGenerator{
		// fields that may be needed here
	}
}
```
Filling in the names as neccessary

Then you can add a new package in `package/dep-tree-gen/internal`, and begin building out the functions. For examples, you can take a look at any of the currently implemented dependency tree generators.


### LAVI cli

Once `dep-tree-gen` work is completed, you can go ahead and start adding the command. You will need to add a new file in the `package/lavi-cli/cmd` package, which would look like the following for a language called `foo`:

```go
// package/lavi-cli/cmd/foo.go
package cmd

import (
	"dep-tree-gen/generator"

	"github.com/spf13/cobra"
)

// fooCmd represents the foo command
var npmCmd = &cobra.Command{
	Use:   "foo",
	Short: "Run LAVI against an foo project",
	Run: func(cmd *cobra.Command, args []string) {
        path, _ := cmd.Flags().GetString("path")
		fooGen := generator.GetFooTreeGenerator(path)

		cds := getCds(cmd, fooGen)
		postCommand(cmd, cds, fooGen)
	},
}

func init() {
	rootCmd.AddCommand(fooCmd)
	fooCmd.Flags().String("path", ".", "Path to project")
}
```
This is assuming the dependency tree generator for foo requires some arg called `path`

Once the command is added, all you have to do is make some minor changes to the API used to serve the local UI, and you're all set!

### LAVI cli API

For a lot of requests the local UI may make, many are language specific. You can take a look at `package/lavi-cli/internal/server/routes.go` to see all the routes and see which ones have language specific operations. Language specific operations are implements in the `package/lavi-cli/internal/repositories` package, which just tells the API how to install packages, get versions, or revert installs. You will see an interface called `ConfigInterface` in a lot of these places, which is just an interface that allows getting information about the current state.

```go
type ConfigInterface interface {
	GetRepository() string
	GetCDS() models.CDS
	GetOriginalCDS() models.CDS
	SetCDS(models.CDS)
	SetOriginalCDS(models.CDS)
	GetGenerator() generator.RepositoryTreeGenerator
	GetCmd() *cobra.Command

	SetVulns(d map[string][]vulnerabilities.Vulnerability)
	GetVulns() map[string][]vulnerabilities.Vulnerability
	GetOriginalVulns() map[string][]vulnerabilities.Vulnerability

	GetRemote() string
}
```