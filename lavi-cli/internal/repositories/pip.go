package repositories

import (
	"dep-tree-gen/models"
	"encoding/json"
	"io/ioutil"
	"lavi/internal/config"
	"lavi/internal/dispatch"
	"net/http"
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

func PipRevert(pythonPath string, cds models.CDS) {
	commands := []string{"-m", "pip", "install"}
	for _, v := range cds.Nodes {
		commands = append(commands, v.Package+"=="+v.Version)
	}
	cmd := exec.Command(pythonPath, commands...)
	err := cmd.Run()
	if err != nil {
		panic(err)
	}
}

func runPipInstall(pythonPath string, packages map[string]string) *exec.Cmd {

	commands := []string{"-m", "pip", "install"}
	for k, v := range packages {
		commands = append(commands, k+"=="+v)
	}

	cmd := exec.Command(pythonPath, commands...)
	return cmd
}

func PipInstall(cfg config.ConfigInterface, pythonPath string, packages map[string]string) string {
	return dispatch.DispatchInstall(cfg, packages, reflect.ValueOf(runPipInstall), reflect.ValueOf(pythonPath), reflect.ValueOf(packages))
}
