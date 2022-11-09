package server

import (
	"dep-tree-gen/common"
	"dep-tree-gen/generator"
	"dep-tree-gen/models"
	"encoding/json"
	"fmt"
	"io/fs"
	"lavi/internal/dispatch"
	"lavi/internal/repositories"
	"lavi/ui"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/spf13/cobra"
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
	OriginalCDS models.CDS
	CDS         models.CDS
	Cmd         *cobra.Command
	Generator   generator.RepositoryTreeGenerator
}

func (s *ServerConfig) SetCDS(cds models.CDS) {
	s.CDS = cds
}

func (s *ServerConfig) SetOriginalCDS(cds models.CDS) {
	s.OriginalCDS = cds
}

func (s *ServerConfig) GetRepository() string {
	return s.OriginalCDS.Repository
}

func (s *ServerConfig) GetCDS() models.CDS {
	return s.CDS
}

func (s *ServerConfig) GetGenerator() generator.RepositoryTreeGenerator {
	return s.Generator
}

type InstallRequest struct {
	Packages map[string]string `json:"packages"`
}

// too lazy to add more error codes
var errorResp = map[string]string{
	"error": "internal server error occured",
}

func CorsWrapper(next func(w http.ResponseWriter, r *http.Request)) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
		w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		if r.Method == "OPTIONS" {
			return
		}
		next(w, r)
	}
}

func PanicWrapper(next func(w http.ResponseWriter, r *http.Request)) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				out, _ := json.Marshal(errorResp)
				w.WriteHeader(500)
				fmt.Fprintf(w, string(out))
			}
		}()
		next(w, r)
	}
}

func JsonResponse(w http.ResponseWriter, r *http.Request, body interface{}) {
	w.Header().Set("Content-Type", "application/json")
	out, err := json.Marshal(body)
	if err != nil {
		panic(err)
	}
	fmt.Fprintf(w, string(out))
}

func HandlerWrapper(handler func(w http.ResponseWriter, r *http.Request)) func(w http.ResponseWriter, r *http.Request) {
	return PanicWrapper(CorsWrapper(handler))
}

func (s *ServerConfig) GetSetCds(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		s.SetCds(w, r)
		return
	}
	s.GetCds(w, r)
	return
}

func (s *ServerConfig) GetCds(w http.ResponseWriter, r *http.Request) {
	JsonResponse(w, r, s.CDS)
}

func (s *ServerConfig) SetCds(w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	var t models.CDS
	err := decoder.Decode(&t)
	if err != nil {
		panic(err)
	}

	if errData, ok := IsUploadedCdsValid(w, r, t, s.CDS); !ok {
		out, _ := json.Marshal(errData)
		w.WriteHeader(400)
		fmt.Fprintf(w, string(out))
		return
	}

	s.SetCDS(t)

	JsonResponse(w, r, t)
}

func (s *ServerConfig) GetOriginalCds(w http.ResponseWriter, r *http.Request) {
	JsonResponse(w, r, s.OriginalCDS)
}

// expects /api/v1/{repoName}/versions
func (s *ServerConfig) GetVersions(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	repoName, ok := vars["repoName"]
	if !ok {
		panic("no repo provided")
	}

	packageName := r.URL.Query().Get("name")

	if repoName == common.PIP_REPO_NAME {
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

// expects /api/v1/{repoName}/install/
func (s *ServerConfig) Install(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	repoName, ok := vars["repoName"]
	if !ok {
		panic("no repo provided")
	}

	decoder := json.NewDecoder(r.Body)
	var t InstallRequest
	err := decoder.Decode(&t)

	if err != nil {
		panic(err)
	}

	if repoName == common.PIP_REPO_NAME {
		pythonPath, _ := s.Cmd.Flags().GetString("python")
		JsonResponse(w, r, map[string]string{"id": repositories.PipInstall(s, pythonPath, t.Packages)})
		return
	}
	if repoName == common.GO_REPO_NAME {
		JsonResponse(w, r, map[string]string{"id": repositories.GoInstall(s, t.Packages)})
		return
	}
	if repoName == common.NPM_REPO_NAME {
		JsonResponse(w, r, map[string]string{"id": repositories.NpmInstall(s, t.Packages)})
		return
	}

	panic("failed")
}

// expects /api/v1/dispatch/status/
func (s *ServerConfig) DispatchStatus(w http.ResponseWriter, r *http.Request) {
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

// expects /api/v1/dispatch/stdout/
func (s *ServerConfig) DispatchStdout(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Query().Get("id")
	f := dispatch.Running[id].StdoutString
	JsonResponse(w, r, map[string]string{
		"stdout": f,
	})
}
