package server

import (
	"dep-tree-gen/common"
	"dep-tree-gen/models"
	"encoding/json"
	"fmt"
	"io/fs"
	"lavi/internal/config"
	"lavi/internal/dispatch"
	"lavi/internal/repositories"
	"lavi/ui"
	"net/http"

	"github.com/gorilla/mux"
)

func RegisterRoutes(server *Server) {
	server.Register("/api/v1/cds", GetCds, "GET")
	server.Register("/api/v1/cds/vulnerabilities", GetCdsVulnerabilities, "GET")
	server.Register("/api/v1/cds", SetCds, "POST")
	server.Register("/api/v1/cds/original", GetOriginalCds, "GET")
	server.Register("/api/v1/cds/original/vulnerabilities", GetOriginalCdsVulns, "GET")
	server.Register("/api/v1/repositories/{repoName}/versions", GetVersions, "GET")
	server.Register("/api/v1/install/{cmdType}", Install, "POST")
	server.Register("/api/v1/dispatch/status", DispatchStatus, "GET")
	server.Register("/api/v1/dispatch/stdout", DispatchStdout, "GET")
	server.router.PathPrefix("/").Handler(http.FileServer(getFileSystem()))
}

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

func GetCds(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	JsonResponse(w, r, s.GetCDS())
}

func SetCds(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	var t models.CDS
	err := decoder.Decode(&t)
	if err != nil {
		panic(err)
	}

	if errData, ok := IsUploadedCdsValid(w, r, t, s.GetCDS()); !ok {
		out, _ := json.Marshal(errData)
		w.WriteHeader(400)
		fmt.Fprintf(w, string(out))
		return
	}

	s.SetCDS(t)

	JsonResponse(w, r, t)
}

func GetOriginalCds(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	JsonResponse(w, r, s.GetOriginalCDS())
}

func GetCdsVulnerabilities(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	JsonResponse(w, r, s.GetVulns())
}

func GetOriginalCdsVulns(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	JsonResponse(w, r, s.GetOriginalVulns())
}

func GetVersions(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	repoName, ok := vars["repoName"]
	if !ok {
		panic("no repo provided")
	}

	packageName := r.URL.Query().Get("name")

	if repoName == common.PIP_REPO_NAME || repoName == common.POETRY_REPO_NAME {
		JsonResponse(w, r, repositories.GetPipVersions(packageName))
		return
	}
	if repoName == common.GO_REPO_NAME {
		JsonResponse(w, r, repositories.GetGoVersions(packageName))
		return
	}
	if repoName == common.NPM_REPO_NAME {
		JsonResponse(w, r, repositories.GetNpmVersions(packageName))
		return
	}

	panic("failed")
}

func Install(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	cmdType, ok := vars["cmdType"]
	if !ok {
		panic("no repo provided")
	}

	decoder := json.NewDecoder(r.Body)
	var t struct {
		Packages map[string]string `json:"packages"`
	}
	err := decoder.Decode(&t)

	if err != nil {
		panic(err)
	}

	if cmdType == common.PIP_CMD_NAME {
		pythonPath, _ := s.GetCmd().Flags().GetString("python")
		JsonResponse(w, r, map[string]string{"id": repositories.PipInstall(s, pythonPath, t.Packages)})
		return
	}
	if cmdType == common.GO_CMD_NAME {
		JsonResponse(w, r, map[string]string{"id": repositories.GoInstall(s, t.Packages)})
		return
	}
	if cmdType == common.NPM_CMD_NAME {
		JsonResponse(w, r, map[string]string{"id": repositories.NpmInstall(s, t.Packages)})
		return
	}
	if cmdType == common.POETRY_CMD_NAME {
		JsonResponse(w, r, map[string]string{"id": repositories.PoetryInstall(s, t.Packages)})
		return
	}

	panic("failed")
}

func DispatchStatus(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	f := dispatch.Running[id]
	err := ""
	if f.Error != nil {
		err = f.Error.Error()
	}
	JsonResponse(w, r, map[string]string{
		"status": f.Status,
		"error":  err,
	})
}

func DispatchStdout(s config.ConfigInterface, w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	f := dispatch.Running[id].StdoutString
	JsonResponse(w, r, map[string]string{
		"stdout": f,
	})
}
