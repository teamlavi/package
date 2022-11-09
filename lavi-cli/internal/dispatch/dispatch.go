package dispatch

import (
	"bufio"
	"dep-tree-gen/common"
	"errors"
	"io"
	"lavi/internal/config"
	"os/exec"
	"reflect"
	"strings"

	"github.com/google/uuid"
)

type Function struct {
	ID           string
	Complete     bool
	Status       string
	Error        error
	StdoutString string
	Handler      reflect.Value
	Args         []reflect.Value
}

var Running = map[string]*Function{}

func Defer(err interface{}, function *Function) {
	if err != nil {
		if e, ok := err.(error); ok {
			function.Error = e
			function.Status = "error"
			return
		}
	}
	function.Status = "success"
}

func RunCommand(cmd *exec.Cmd, function *Function) {
	cmd.Stderr = cmd.Stdout
	stdout, _ := cmd.StdoutPipe()

	cmd.Start()

	reader := bufio.NewReader(stdout)
	line, err := reader.ReadString('\n')
	for err == nil {
		function.StdoutString += line
		line, err = reader.ReadString('\n')
	}
	if err != nil && !errors.Is(err, io.EOF) {
		panic(err)
	}
	cmd.Wait()
}

func DispatchInstall(cfg config.ConfigInterface, packages map[string]string, handler reflect.Value, args ...reflect.Value) string {
	function := &Function{
		ID:       uuid.NewString(),
		Complete: false,
		Handler:  handler,
		Status:   "installing",
		Args:     args,
	}
	Running[function.ID] = function
	go func() {
		defer func() {
			Defer(recover(), function)
		}()
		out := function.Handler.Call(function.Args)
		cmd := out[0].Interface().(*exec.Cmd)

		function.StdoutString += cmd.Path + strings.Join(cmd.Args, " ")

		RunCommand(cmd, function)

		if cfg.GetRepository() == common.GO_REPO_NAME {
			function.StdoutString += "running go mod tidy\r\n"
			RunCommand(exec.Command("go", "mod", "tidy"), function)
		}

		function.Status = "vulns"

		cds := cfg.GetCDS()
		for _, d := range cds.Root.Dependencies {
			data := cds.Nodes[d]
			if _, has := packages[data.Package]; !has {
				packages[data.Package] = data.Version
			}
		}

		gen := cfg.GetGenerator().GetCDSForPackages(packages)
		cfg.SetCDS(gen)
		function.Status = "success"

	}()
	return function.ID
}

func Clear(id string) {
	delete(Running, id)
}
