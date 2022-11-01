package golang

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

func GenerateTree(path string) {
	if _, err := os.Stat(filepath.Join(path, "go.mod")); err != nil {
		panic("project must contain go.mod")
	}
	tree := generateTree(path)
	modFile, err := ioutil.ReadFile(filepath.Join(path, "go.mod"))
	if err != nil {
		panic(err)
	}

	name := strings.Split(strings.Split(string(modFile), "\n")[0], " ")[1]

	cds := outputTreeToCds(name, tree)
	file, _ := json.MarshalIndent(cds, "", " ")
	_ = ioutil.WriteFile("test.json", file, 0644)
}

func generateTree(path string) string {
	cmd := exec.Command("go", "mod", "graph")
	cmd.Dir = path
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		panic(err)
	}
	return out.String()
}
