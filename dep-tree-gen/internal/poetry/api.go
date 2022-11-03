package poetry

import (
	"dep-tree-gen/models"
)

type PoetryTreeGenerator struct {
	Path string
}

func (g PoetryTreeGenerator) GetCDS() models.CDS {
	verifyPoetryDependency()
	lockFile := getPoetryLockFile(g.Path)
	pyproject := getPoetryTomlFileDependencues(g.Path)

	return poetryLockFileToCds(lockFile, pyproject)
}
