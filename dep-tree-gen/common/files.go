package common

import (
	"fmt"
	"io"
	"log"
	"os"

	"github.com/google/uuid"
)

func BackupFile(filename string) string {
	newName := "lavi-backup-" + uuid.NewString() + "-" + filename
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

var Backedup = map[string]string{}

func BackupToTemp(filename string) error {
	f, err := os.CreateTemp("", "lavi-backup-")
	if err != nil {
		return err
	}

	defer f.Close()

	src, err := os.Open(filename)

	if err != nil {
		return err
	}

	defer src.Close()

	_, err = io.Copy(f, src)

	if err != nil {
		return err
	}

	name := f.Name()

	Backedup[filename] = name

	return nil
}

func RestoreFromTemp(filename string) error {
	backupName := Backedup[filename]
	src, err := os.Open(backupName)
	if err != nil {
		return err
	}
	defer src.Close()

	dst, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer src.Close()

	_, err = io.Copy(dst, src)

	if err != nil {
		return err
	}

	return nil
}
