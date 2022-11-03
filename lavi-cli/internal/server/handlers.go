package server

import (
	"io/fs"
	"lavi-cli/ui"
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
