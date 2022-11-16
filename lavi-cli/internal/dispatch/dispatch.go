package dispatch

import (
	"bufio"
	"dep-tree-gen/common"
	"errors"
	"fmt"
	"io"
	"lavi/internal/config"
	"lavi/internal/vulnerabilities"
	"os/exec"
	"reflect"
	"sync"

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
	var wg sync.WaitGroup

	stdout, _ := cmd.StdoutPipe()
	stderr, _ := cmd.StderrPipe()

	cmd.Start()

	scannerStdout := bufio.NewReader(stdout)
	wg.Add(1)
	go func() {
		line, err := scannerStdout.ReadString('\n')
		for err == nil {
			function.StdoutString += line
			line, err = scannerStdout.ReadString('\n')
		}
		if err != nil && !errors.Is(err, io.EOF) {
			wg.Done()
			panic(err)
		}
		wg.Done()
	}()
	scannerStderr := bufio.NewReader(stderr)
	wg.Add(1)
	go func() {
		line, err := scannerStderr.ReadString('\n')
		for err == nil {
			function.StdoutString += line
			line, err = scannerStderr.ReadString('\n')
		}
		if err != nil && !errors.Is(err, io.EOF) {
			wg.Done()
			panic(err)
		}
		wg.Done()
	}()

	wg.Wait()
	if err := cmd.Wait(); err != nil {
		function.StdoutString += "Failed to install selected changes. Are you sure the package and version name combinations are correct?\r\n"
		panic(err)
	}
}

// dispatches a goroutine thread that can be identified by the id returned
// eventually, will probably limit to just one goroutine since we probably dont want multiple installs
// in a single session
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

		pkgIds := []string{}
		for id, _ := range gen.Nodes {
			pkgIds = append(pkgIds, id)
		}

		function.StdoutString += fmt.Sprintf("Scanning %d packages for vulnerabilities\r\n", len(pkgIds))

		all := []vulnerabilities.BatchVulnerabilityResponse{}
		c := 0
		for i := 0; i < len(pkgIds); i += 100 {
			slice, count := vulnerabilities.GrabSlice(i, i+100, pkgIds)
			all = append(all, vulnerabilities.ScanSet(slice, false))
			c += count
			if c > len(pkgIds) {
				c = len(pkgIds)
			}
			function.StdoutString += fmt.Sprintf("Completed %d packages\r\n", c)
		}
		function.StdoutString += "Finished scanning\r\n"

		vulns := vulnerabilities.CleanupScanResults(all)
		cleanVulns := vulnerabilities.ConvertToCleanResponse(vulns)

		cfg.SetCDS(gen)
		cfg.SetVulns(cleanVulns)
		function.Status = "success"

	}()
	return function.ID
}

func DispatchRevert(cfg config.ConfigInterface, handler reflect.Value) string {
	function := &Function{
		ID:       uuid.NewString(),
		Complete: false,
		Handler:  handler,
		Status:   "installing",
	}
	Running[function.ID] = function
	go func() {
		defer func() {
			Defer(recover(), function)
		}()

		err := cfg.GetGenerator().RestoreFiles()
		if err != nil {
			function.StdoutString += "failed to restore files\r\n"
			function.Status = "error"
			panic("failed to restore files")
		}

		out := function.Handler.Call([]reflect.Value{})
		cmd := out[0].Interface().(*exec.Cmd)

		RunCommand(cmd, function)

		cfg.SetCDS(cfg.GetOriginalCDS())
		cfg.SetVulns(cfg.GetOriginalVulns())
		function.Status = "success"

	}()
	return function.ID
}

func Clear(id string) {
	delete(Running, id)
}
