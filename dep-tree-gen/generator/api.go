package generator

import "dep-tree-gen/models"

type RepositoryTreeGenerator interface {
	GetCDS() models.CDS
	// allows for consistent calls in a single function - really on neccessary for pip
	// since thats the only repo that doesnt automatically update some dependency/lock file
	GetCDSForPackages(map[string]string) models.CDS

	// run single package generation mode
	GenerateSinglePackageCds(pkg, version string) models.CDS

	BackupFiles() error
	RestoreFiles() error
}
