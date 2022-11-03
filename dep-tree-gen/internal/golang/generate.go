package golang

import (
	"bytes"
	"os/exec"
)

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
