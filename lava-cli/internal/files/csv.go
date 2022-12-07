package files

import (
	"encoding/csv"
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

var letters = []rune("1234567890")

func randSeq(n int) string {
	rand.Seed(time.Now().Unix())
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

func SaveCSV(filename string, data [][]string) error {
	if !(strings.HasSuffix(filename, ".csv")) {
		filename += ".csv"
	}
	if filename == "lava-response.csv" {
		filename = fmt.Sprintf("lava-response-%s.csv", randSeq(4))
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
	fmt.Printf("wrote csv to %s\n", filename)
	return nil
}
