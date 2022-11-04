package server

import (
	"dep-tree-gen/models"
	"encoding/json"
	"fmt"
	"io/fs"
	"lavi/ui"
	"net/http"
)

func getFileSystem() http.FileSystem {

	// Get the build subdirectory as the
	// root directory so that it can be passed
	// to the http.FileServer
	fsys, err := fs.Sub(ui.Assets, "build")
	if err != nil {
		panic(err)
	}

	return http.FS(fsys)
}

type ServerConfig struct {
	CDS models.CDS
}

func (s ServerConfig) GetCds(w http.ResponseWriter, r *http.Request) {
	out, _ := json.Marshal(s.CDS)
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, string(out))
}
