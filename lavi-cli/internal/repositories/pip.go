package repositories

import (
	"encoding/json"
	"io/ioutil"
	"lavi/internal/config"
	"lavi/internal/dispatch"
	"net/http"
	"os"
	"os/exec"
	"reflect"
)

// were actually gonna call an api for this because the pip solution isnt clean and I'm lazy
// GET /repositories/{repoName}/packages/{packageName}/versions => array of versions (in order preferably)
// want api designed this way because it allows for easy expansion without having to rewrite a bunch of endpoints
// expansion into -> listing packages, getting a single package, getting a single package + version combo, etc

// for now, just gonna call pypi
// https://pypi.org/pypi/{name}/json

type PypiResponse struct {
	Releases map[string]interface{} `json:"releases"` // only part I care about
}

func GetPipVersions(packageName string) []string {
	url := "https://pypi.org/pypi/" + packageName + "/json"
	response, err := http.Get(url)
	if err != nil {
		panic(err)
	}

	defer response.Body.Close()
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		panic(err)
	}
	var data PypiResponse
	err = json.Unmarshal(body, &data)
	if err != nil {
		panic(err)
	}

	out := []string{}
	for k, _ := range data.Releases {
		out = append(out, k)
	}

	return out
}

func PipRevert(cfg config.ConfigInterface, pythonPath string, reqPath string) string {
	return dispatch.DispatchRevert(cfg, reflect.ValueOf(func() *exec.Cmd {
		return exec.Command(pythonPath, "-m", "pip", "install", "-r", reqPath)
	}))
}

func runPipInstall(pythonPath string, requirementsPath string, packages map[string]string) *exec.Cmd {
	pkgs := ""
	commands := []string{"-m", "pip", "install", "-r", requirementsPath}
	for k, v := range packages {
		pkgs = pkgs + k + "==" + v + "\n"
	}
	// need to write to requirements.txt
	if err := os.WriteFile(requirementsPath, []byte(pkgs), 0666); err != nil {
		panic(err)
	}

	cmd := exec.Command(pythonPath, commands...)
	return cmd
}

func PipInstall(cfg config.ConfigInterface, pythonPath, requirementsPath string, packages map[string]string) string {
	allPkgs := map[string]string{}
	cds := cfg.GetCDS()
	for _, id := range cds.Root.Dependencies {
		node := cds.Nodes[id]
		if _, exists := packages[node.Package]; exists {
			allPkgs[node.Package] = packages[node.Package]
		} else {
			allPkgs[node.Package] = node.Version
		}
	}
	return dispatch.DispatchInstall(cfg, allPkgs, reflect.ValueOf(runPipInstall), reflect.ValueOf(pythonPath), reflect.ValueOf(requirementsPath), reflect.ValueOf(allPkgs))
}
