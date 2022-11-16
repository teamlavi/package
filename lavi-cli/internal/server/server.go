package server

import (
	"encoding/json"
	"fmt"
	"lavi/internal/config"
	"net/http"

	"github.com/gorilla/mux"
)

type Server struct {
	cfg    config.ConfigInterface
	router *mux.Router
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

func CfgWrapper(cfg config.ConfigInterface, next func(cfg config.ConfigInterface, w http.ResponseWriter, r *http.Request)) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		next(cfg, w, r)
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

func New(config *ServerConfig) *Server {
	return &Server{
		cfg:    config,
		router: mux.NewRouter(),
	}
}

func (s *Server) Cfg() config.ConfigInterface {
	return s.cfg
}

func (s *Server) Register(path string, handler func(cfg config.ConfigInterface, w http.ResponseWriter, r *http.Request), methods ...string) {
	methods = append(methods, "OPTIONS")
	wrappedHandler := CfgWrapper(s.cfg, handler)
	s.router.HandleFunc(path, HandlerWrapper(wrappedHandler)).Methods(methods...)
}

func (s *Server) Serve(port string) error {
	return http.ListenAndServe(port, s.router)
}
