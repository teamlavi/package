package pip

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"
)

// using this so I dont have to rewrite stuff https://pypi.org/project/pipdeptree/\
// this code just orchestrates calling pipdeptree
func verifyPipDepTreeInstall(pythonPath string) {
	cmd := exec.Command(pythonPath, "-m", "pip", "install", "pipdeptree")
	err := cmd.Run()
	if err != nil {
		log.Fatal(err)
	}
}

// requirements files can be super complex, this is a VERY naive implementation
// https://pip.pypa.io/en/stable/reference/requirements-file-format/
func getPackageNamesFromReq(path string) []string {
	dat, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}

	pkgs := []string{}

	for _, l := range strings.Split(string(dat), "\n") {
		if l != "" {
			pkgs = append(pkgs, strings.Split(l, "==")[0])
		}
	}
	return pkgs
}

func callPDP(pkgs []string, pythonPath string) []PDPObject {

	cmd := exec.Command(pythonPath, "-m", "pipdeptree", "-p", strings.Join(pkgs, ","), "--json")
	var out bytes.Buffer
	cmd.Stdout = &out

	err := cmd.Run()
	if err != nil {
		log.Fatal(err)
	}

	var pdpOutput []PDPObject
	err = json.Unmarshal(out.Bytes(), &pdpOutput)
	if err != nil {
		log.Fatal(err)
	}
	return pdpOutput
}

func getInstalledPythonDistributions() {
	cmd := exec.Command("python", "-m", "pip", "freeze")
	var out bytes.Buffer
	cmd.Stdout = &out

	err := cmd.Run()
	if err != nil {
		log.Fatal(err)
	}

	dists := out.String()
	for i, l := range strings.Split(dists, "\n") {
		fmt.Println(i, l)
	}

}
