package golang

import (
	"bytes"
	"log"
	"os/exec"
)

func generateTree(path string) string {
	cmd := exec.Command("go", "mod", "graph")
	cmd.Dir = path
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		log.Fatal("failed to call `go mod graph` for project")
	}
	return out.String()
}
