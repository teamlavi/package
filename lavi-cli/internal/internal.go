package internal

import (
	"bufio"
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
	"fmt"
	"lavi/internal/server"
	"lavi/internal/vulnerabilities"
	"log"
	"net"
	"os"
	"os/exec"
	"runtime"
	"strconv"
	"strings"

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

func Serve(cmd *cobra.Command, cds models.CDS, gen generator.RepositoryTreeGenerator, vulnData map[string][]vulnerabilities.Vulnerability) {
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
	})

	server.RegisterRoutes(api)

	stringPort := ":" + strconv.Itoa(port)

	openbrowser("http://localhost" + stringPort)

	api.Serve(stringPort)
}
