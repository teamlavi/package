package dispatch

import (
	"bufio"
	"errors"
	"io"
	"lavi/internal/config"
	"os/exec"
	"reflect"

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

func Dispatch(handler reflect.Value, args ...reflect.Value) string {
	function := &Function{
		ID:       uuid.NewString(),
		Complete: false,
		Handler:  handler,
		Args:     args,
	}
	Running[function.ID] = function
	go func() {
		defer func() {
			Defer(recover(), function)
		}()
		function.Handler.Call(function.Args)
	}()
	return function.ID
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
		stdout, _ := cmd.StdoutPipe()
		cmd.Stderr = cmd.Stdout

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
