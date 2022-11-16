package files

import (
	"encoding/csv"
	"os"
	"strings"
)

func SaveCSV(filename string, data [][]string) error {
	if !(strings.HasSuffix(filename, ".csv")) {
		filename += ".csv"
	}
	csvFile, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer csvFile.Close()
	csvwriter := csv.NewWriter(csvFile)

	for _, empRow := range data {
		_ = csvwriter.Write(empRow)
	}

	csvwriter.Flush()
	return nil
}
