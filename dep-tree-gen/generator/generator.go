package generator

import (
	"dep-tree-gen/internal/golang"
	"dep-tree-gen/internal/npm"
	"dep-tree-gen/internal/pip"
	"dep-tree-gen/internal/poetry"
)

func GetGoTreeGenerator(path string) RepositoryTreeGenerator {
	return golang.GolangTreeGenerator{
		Path: path,
	}
}

func GetNpmTreeGenerator(path string) RepositoryTreeGenerator {
	return npm.NpmTreeGenerator{
		Path: path,
	}
}

func GetPipTreeGenerator(path, pythonPath string) RepositoryTreeGenerator {
	return pip.PipTreeGenerator{
		Path:       path,
		PythonPath: pythonPath,
	}
}

func GetPoetryTreeGenerator(path string) RepositoryTreeGenerator {
	return poetry.PoetryTreeGenerator{
		Path: path,
	}
}
