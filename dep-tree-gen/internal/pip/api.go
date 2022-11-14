package pip

import (
	"bufio"
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"fmt"
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
	verifyPipDepTreeInstall(g.PythonPath)
	pkgs := getPackageNamesFromReq(g.Path)

	tree := callPDP(pkgs, g.PythonPath)
	cds := pdpObjectArrToCds(tree, pkgs)

	return cds
}

func (g PipTreeGenerator) GetCDSForPackages(pkgs map[string]string) models.CDS {
	data := []string{}
	for k, _ := range pkgs {
		data = append(data, k)
	}
	tree := callPDP(data, g.PythonPath)
	cds := pdpObjectArrToCds(tree, data)
	return cds
}

func (g PipTreeGenerator) Revert(cds models.CDS) {
	pythonPath := g.PythonPath
	cmd := []string{"-m", "pip", "install"}
	for _, node := range cds.Nodes {
		cmd = append(cmd, fmt.Sprintf("%s==%s", node.Package, node.Version))
	}

	out := exec.Command(pythonPath, cmd...)
	err := out.Run()
	if err != nil {
		log.Fatal(err)
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
	if err != nil {
		log.Fatal("Failed to install " + fmt.Sprintf("%s==%s", pkg, version) + ". Are you sure the package and version name combination is correct?")

	}
	cmd.Wait()

	// now we get the new cds
	cds := g.GetCDS()

	// then revert the installation
	fmt.Println("reverting installation")
	g.Revert(currentCds)

	// restore file if it exists
	common.RestoreFile(backupReq, "requirements.txt")
	return cds
}
