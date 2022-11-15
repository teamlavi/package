package repositories

import (
	"bytes"
	"encoding/json"
	"lavi/internal/config"
	"lavi/internal/dispatch"
	"os/exec"
	"reflect"
)

// eventually we will probably defer to using an api but for now we rocking with this
func GetNpmVersions(packageName string) []string {
	cmd := exec.Command("npm", "show", packageName+"@*", "version", "--json")
	var out bytes.Buffer
	cmd.Stdout = &out

	err := cmd.Run()
	if err != nil {
		panic(err)
	}
	var versions []string
	err = json.Unmarshal(out.Bytes(), &versions)
	if err != nil {
		panic(err)
	}
	return versions
}

func NpmRevert(cfg config.ConfigInterface) string {
	return NpmInstall(cfg, CDSToPkgMap(cfg.GetOriginalCDS()))
}

func runNpmInstall(packages map[string]string) *exec.Cmd {

	commands := []string{"install", "--progress=false"}
	for k, v := range packages {
		commands = append(commands, k+"@"+v)
	}

	cmd := exec.Command("npm", commands...)
	return cmd
}

func NpmInstall(cfg config.ConfigInterface, packages map[string]string) string {
	return dispatch.DispatchInstall(cfg, packages, reflect.ValueOf(runNpmInstall), reflect.ValueOf(packages))
}
