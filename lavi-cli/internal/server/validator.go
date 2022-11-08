package server

import (
	"dep-tree-gen/models"
	"dep-tree-gen/utils"
	"fmt"
	"net/http"
)

func IsUploadedCdsValid(w http.ResponseWriter, r *http.Request, uploaded, expected models.CDS) (map[string]string, bool) {
	if uploaded.CmdType != expected.CmdType {
		return map[string]string{"error": fmt.Sprintf("Provided command type (%s) does not match expected (%s)", uploaded.CmdType, expected.CmdType)}, false
	}
	if uploaded.Repository != expected.Repository {
		return map[string]string{"error": fmt.Sprintf("Provided repository (%s) does not match expected (%s)", uploaded.Repository, expected.Repository)}, false
	}

	for id, data := range uploaded.Nodes {
		expectedHash := utils.GenerateID(data.Package, data.Version, uploaded.Repository)
		if expectedHash != id {
			return map[string]string{"error": fmt.Sprintf("Tree validation failed for package %s==%s", data.Package, data.Version)}, false
		}
	}

	return nil, true
}
