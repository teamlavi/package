package common

import (
	"fmt"
	"log"
	"os"
)

func BackupFile(filename string) string {
	newName := "lavi-backup-" + filename
	if err := os.Rename(filename, newName); err != nil && !os.IsNotExist(err) {
		log.Fatal(fmt.Sprintf("failed to backup %s as %s", filename, newName))
	} else if os.IsNotExist(err) {
		return ""
	}
	return newName
}

func RestoreFile(backupName, filename string) {
	if backupName == "" {
		// means the file never existed in the first place, therefore just delete new file
		os.Remove(filename)
		return
	}
	// we assume that this file exists
	if err := os.Remove(filename); err != nil {
		log.Fatal(fmt.Sprintf("failed to delete temporary %s", filename))
	}
	if err := os.Rename(backupName, filename); err != nil {
		log.Fatal(fmt.Sprintf("failed to restore %s as %s", backupName, filename))
	}
}
