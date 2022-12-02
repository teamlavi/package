package internal

import (
	"bufio"
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
	"fmt"
	"lavi/internal/dispatch"
	"lavi/internal/server"
	"lavi/internal/vulnerabilities"
	"log"
	"net"
	"os"
	"os/exec"
	"os/signal"
	"reflect"
	"runtime"
	"strconv"
	"strings"
	"syscall"
	"time"

	"github.com/spf13/cobra"
)

func openbrowser(url string) {
	var err error

	switch runtime.GOOS {
	case "linux":
		err = exec.Command("xdg-open", url).Start()
	case "windows":
		err = exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		err = exec.Command("open", url).Start()
	default:
		err = fmt.Errorf("unsupported platform")
	}
	if err != nil {
		log.Fatal(err)
	}

}

func isPortOpen(port int) bool {
	ln, err := net.Listen("tcp", ":"+strconv.Itoa(port))

	if err != nil {
		return false
	}

	ln.Close()
	return true
}

func WatchId(id string) {
	seen := 0
	for {
		function := dispatch.Running[id]
		if function.Status == "error" {
			fmt.Println("reverting failed")
			fmt.Println(function.Error.Error())
			return
		}

		if function.Status == "success" {
			return
		}

		stdout := function.StdoutString
		fmt.Print(stdout[seen:])
		seen = len(stdout)

		time.Sleep(3 * time.Second)
	}
}

func Serve(cmd *cobra.Command, cds models.CDS, gen generator.RepositoryTreeGenerator, vulnData map[string][]vulnerabilities.Vulnerability, remote string) {
	port := 8080

	for {
		if !isPortOpen(port) {
			r := bufio.NewReader(os.Stdin)
			fmt.Printf("Port %d is in use. Try a different port? [Y/n]: ", port)

			res, err := r.ReadString('\n')
			if err != nil {
				log.Fatal(err)
			}

			// Empty input (i.e. "\n")
			if len(res) < 2 {
				port += 1
				continue
			}

			if strings.ToLower(strings.TrimSpace(res))[0] != 'y' {
				os.Exit(0)
			} else {
				port += 1
			}
		} else {
			break
		}
	}

	api := server.New(&server.ServerConfig{
		CDS:                        cds,
		OriginalCDS:                cds,
		Cmd:                        cmd,
		Generator:                  gen,
		CDSVulnerabilities:         vulnData,
		OriginalCDSVulnerabilities: vulnData,
		Remote:                     remote,
	})

	server.RegisterRoutes(api)

	stringPort := ":" + strconv.Itoa(port)

	openbrowser("http://localhost" + stringPort)

	err := gen.BackupFiles()
	if err != nil {
		log.Fatal("failed to backup files")
	}
	var gracefulStop = make(chan os.Signal)
	signal.Notify(gracefulStop, syscall.SIGTERM)
	signal.Notify(gracefulStop, syscall.SIGINT)

	go func() {
		<-gracefulStop
		cfg := api.Cfg()
		if !reflect.DeepEqual(cfg.GetCDS(), cfg.GetOriginalCDS()) {
			r := bufio.NewReader(os.Stdin)
			fmt.Print("You are exiting with a modified dependency tree. Would you like to revert back to the original tree? [Y/n]: ")

			res, err := r.ReadString('\n')
			if err != nil {
				log.Fatal(err)
			}

			if len(res) < 2 {
				fmt.Println("reverting")
				id := server.RevertCommon(cfg, cfg.GetCDS().CmdType)
				WatchId(id)
			}

			if strings.ToLower(strings.TrimSpace(res))[0] != 'y' {
				os.Exit(0)
			} else {
				fmt.Println("reverting")
				id := server.RevertCommon(cfg, cfg.GetCDS().CmdType)
				WatchId(id)
			}
		}

		os.Exit(0)
	}()

	api.Serve(stringPort)
}
