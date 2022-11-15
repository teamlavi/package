package repositories

import (
	"bytes"
	"lavi/internal/config"
	"lavi/internal/dispatch"
	"os/exec"
	"reflect"
	"strings"
)

// eventually we will probably defer to using an api but for now we rocking with this
func GetGoVersions(packageName string) []string {
	cmd := exec.Command("go", "list", "-m", "-versions", packageName)
	var out bytes.Buffer
	cmd.Stdout = &out

	err := cmd.Run()
	if err != nil {
		panic(err)
	}
	txt := strings.ReplaceAll(string(out.Bytes()), packageName, "")
	txt = strings.ReplaceAll(txt, "\n", "")
	return strings.Split(txt, " ")
}

func GoRevert(cfg config.ConfigInterface) string {
	return GoInstall(cfg, CDSToPkgMap(cfg.GetOriginalCDS()))
}

func runGoInstall(packages map[string]string) *exec.Cmd {

	commands := []string{"get", "-v"}
	for k, v := range packages {
		commands = append(commands, k+"@"+v)
	}

	cmd := exec.Command("go", commands...)
	return cmd
}

func GoInstall(cfg config.ConfigInterface, packages map[string]string) string {
	return dispatch.DispatchInstall(cfg, packages, reflect.ValueOf(runGoInstall), reflect.ValueOf(packages))
}
