package generator

import (
	"dep-tree-gen/internal/golang"
	"dep-tree-gen/internal/npm"
	"dep-tree-gen/internal/pip"
)

func GeneratePipTree(path, pythonPath string) { // https://pypi.org/project/pipdeptree/
	pip.GenerateTree(path, pythonPath)
}

func GenerateNpmTree(path string) {
	npm.GenerateTree(path)
}
func GenerateGoTree(path string) {
	golang.GenerateTree(path)
}
