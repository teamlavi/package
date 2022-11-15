package repositories

import (
	"lavi/internal/config"
	"lavi/internal/dispatch"
	"os/exec"
	"reflect"
)

func PoetryRevert(cfg config.ConfigInterface) string {
	return PoetryInstall(cfg, CDSToPkgMap(cfg.GetOriginalCDS()))
}

func runPoetryInstall(packages map[string]string) *exec.Cmd {

	commands := []string{"add"}
	for k, v := range packages {
		commands = append(commands, k+"=="+v)
	}

	cmd := exec.Command("poetry", commands...)
	return cmd
}

func PoetryInstall(cfg config.ConfigInterface, packages map[string]string) string {
	return dispatch.DispatchInstall(cfg, packages, reflect.ValueOf(runPoetryInstall), reflect.ValueOf(packages))
}
