package pip

import (
	"bufio"
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"errors"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
)

type PipTreeGenerator struct {
	// path is a path to requirements.txt
	Path string
	// PyPath can be either the alias to call python or the path to executable
	PythonPath string
}

func (g PipTreeGenerator) GetCDS() models.CDS {
	common.HasExecutableFailOut(g.PythonPath)
	verifyPipDepTreeInstall(g.PythonPath)
	pkgs := getPackageNamesFromReq(g.Path)

	tree := callPDP(pkgs, g.PythonPath)
	cds := pdpObjectArrToCds(tree, pkgs)

	return cds
}

func (g PipTreeGenerator) GetCDSForPackages(pkgs map[string]string) models.CDS {
	common.HasExecutableFailOut(g.PythonPath)
	data := []string{}
	for k, _ := range pkgs {
		data = append(data, k)
	}
	tree := callPDP(data, g.PythonPath)
	cds := pdpObjectArrToCds(tree, data)
	return cds
}

func (g PipTreeGenerator) Revert(cds models.CDS) {
	common.HasExecutableFailOut(g.PythonPath)
	pythonPath := g.PythonPath
	command := []string{"-m", "pip", "install"}
	if len(cds.Nodes) == 0 {
		return
	}
	for _, node := range cds.Nodes {
		command = append(command, fmt.Sprintf("%s==%s", node.Package, node.Version))
	}
	cmd := exec.Command(pythonPath, command...)
	cmd.Stderr = cmd.Stdout
	stdout, _ := cmd.StdoutPipe()

	cmd.Start()

	reader := bufio.NewReader(stdout)
	line, err := reader.ReadString('\n')
	for err == nil {
		fmt.Print(line)
		line, err = reader.ReadString('\n')
	}
	if err != nil && !errors.Is(err, io.EOF) {
		log.Fatal("unknown error occured")
	}
	if err = cmd.Wait(); err != nil {
		log.Fatal("Failed to revert installation")
	}
}

func (g PipTreeGenerator) GenerateSinglePackageCds(pkg, version string) models.CDS {

	pythonPath := g.PythonPath

	fileData := fmt.Sprintf(`
%s==%s
		`, pkg, version)

	currentCds := g.GetCDSForPackages(map[string]string{pkg: version})

	backupReq := common.BackupFile("requirements.txt")

	fileBytes := []byte(fileData)
	err := os.WriteFile("requirements.txt", fileBytes, 0644)
	if err != nil {
		log.Fatal("failed to write new requirements.txt")
	}

	// need to install the dependencies for the generator to work
	fmt.Println("installing " + fmt.Sprintf("%s==%s", pkg, version))
	cmd := exec.Command(pythonPath, "-m", "pip", "install", fmt.Sprintf("%s==%s", pkg, version))
	cmd.Stderr = cmd.Stdout
	stdout, _ := cmd.StdoutPipe()

	cmd.Start()

	reader := bufio.NewReader(stdout)
	line, err := reader.ReadString('\n')
	for err == nil {
		fmt.Print(line)
		line, err = reader.ReadString('\n')
	}
	if err != nil && !errors.Is(err, io.EOF) {
		log.Fatal("unknown error occured")
	}
	if err = cmd.Wait(); err != nil {
		log.Fatal("Failed to install " + fmt.Sprintf("%s==%s", pkg, version) + ". Are you sure the package and version name combination is correct?")
	}

	// now we get the new cds
	cds := g.GetCDS()

	// then revert the installation
	fmt.Println("reverting installation")
	g.Revert(currentCds)

	// restore file if it exists
	common.RestoreFile(backupReq, "requirements.txt")
	return cds
}
