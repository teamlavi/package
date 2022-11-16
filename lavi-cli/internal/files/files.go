package files

import (
	"io"
	"os"
)

var Backedup = map[string]string{}

func Backup(filename string) (string, error) {
	f, err := os.CreateTemp("", "lavi-backup-")
	if err != nil {
		return "", err
	}

	defer f.Close()

	src, err := os.Open(filename)

	if err != nil {
		return "", err
	}

	defer src.Close()

	_, err = io.Copy(f, src)

	if err != nil {
		return "", err
	}

	name := f.Name()

	Backedup[filename] = name

	return name, nil
}

func Restore(filename string) error {
	backupName := Backedup[filename]
	src, err := os.Open(backupName)
	if err != nil {
		return err
	}
	defer src.Close()

	dst, err := os.Open(filename)
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
