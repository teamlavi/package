package server

import (
	"bufio"
	"dep-tree-gen/models"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"
)

func isPortOpen(port int) bool {
	ln, err := net.Listen("tcp", ":"+strconv.Itoa(port))

	if err != nil {
		return false
	}

	ln.Close()
	return true
}

func Serve(cds models.CDS) {
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

	config := ServerConfig{
		CDS: cds,
	}

	http.HandleFunc("/api/v1/cds", config.GetCds)
	http.Handle("/", http.FileServer(getFileSystem()))

	openbrowser("http://localhost:" + strconv.Itoa(port))

	err := http.ListenAndServe(":"+strconv.Itoa(port), nil)
	if err != nil {
		log.Fatal("failed to start api")
	}
}
