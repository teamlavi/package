package generator

import (
	"dep-tree-gen/internal"
	"dep-tree-gen/internal/golang"
	"dep-tree-gen/internal/npm"
	"dep-tree-gen/internal/pip"
	"dep-tree-gen/internal/poetry"
)

func GetGoTreeGenerator(path string) internal.RepositoryTreeGenerator {
	return golang.GolangTreeGenerator{
		Path: path,
	}
}

func GetNpmTreeGenerator(path string) internal.RepositoryTreeGenerator {
	return npm.NpmTreeGenerator{
		Path: path,
	}
}

func GetPipTreeGenerator(path, pythonPath string) internal.RepositoryTreeGenerator {
	return pip.PipTreeGenerator{
		Path:       path,
		PythonPath: pythonPath,
	}
}

func GetPoetryTreeGenerator(path string) internal.RepositoryTreeGenerator {
	return poetry.PoetryTreeGenerator{
		Path: path,
	}
}
