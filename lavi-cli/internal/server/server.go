package server

import (
	"bufio"
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
	"github.com/spf13/cobra"
)

func isPortOpen(port int) bool {
	ln, err := net.Listen("tcp", ":"+strconv.Itoa(port))

	if err != nil {
		return false
	}

	ln.Close()
	return true
}

func Serve(cmd *cobra.Command, cds models.CDS, gen generator.RepositoryTreeGenerator) {
	port := 8080

	for {
		if !isPortOpen(port) {
			r := bufio.NewReader(os.Stdin)
			fmt.Printf("Port %s is in use. Try a different port? [Y/n]: ", port)

			res, err := r.ReadString('\n')
			if err != nil {
				log.Fatal(err)
			}

			// Empty input (i.e. "\n")
			if len(res) < 2 {
				port += 1
			}

			if strings.ToLower(strings.TrimSpace(res))[0] != 'y' {
				os.Exit(0)
			}
		} else {
			break
		}
	}

	config := &ServerConfig{
		CDS:         cds,
		OriginalCDS: cds,
		Cmd:         cmd,
		Generator:   gen,
	}

	r := mux.NewRouter()

	r.HandleFunc("/api/v1/cds", HandlerWrapper(config.GetSetCds))
	r.HandleFunc("/api/v1/cds/original", HandlerWrapper(config.GetOriginalCds))
	r.HandleFunc("/api/v1/repositories/{repoName}/versions", HandlerWrapper(config.GetVersions))
	r.HandleFunc("/api/v1/repositories/{repoName}/install", HandlerWrapper(config.Install)) //.Methods("POST", "OPTIONS")
	r.HandleFunc("/api/v1/dispatch/status", HandlerWrapper(config.DispatchStatus))
	r.HandleFunc("/api/v1/dispatch/stdout", HandlerWrapper(config.DispatchStdout))
	r.PathPrefix("/").Handler(http.FileServer(getFileSystem()))

	openbrowser("http://localhost:" + strconv.Itoa(port))

	err := http.ListenAndServe(":"+strconv.Itoa(port), r)
	if err != nil {
		log.Fatal("failed to start api")
	}
}
