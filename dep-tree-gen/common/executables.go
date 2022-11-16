package common

import (
	"log"
	"os/exec"
)

func HasExecutableFailOut(name string) {
	_, err := exec.LookPath(name)
	if err != nil {
		log.Fatalf("Looks like executable '%s' does not exist. Are you sure it can be accessed from the terminal?", name)
	}
}
