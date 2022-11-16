package models

import (
	"fmt"
)

type LavaRequest struct {
	Repo         Repo     `json:"repo"`
	Packages     []string `json:"packages,omitempty"`
	Offset       int      `json:"offset"`
	Limit        int      `json:"limit"`
	MinDownloads int      `json:"minDownloads"`
	Level        Level    `json:"levels"`
	Status       Status   `json:"status"`
}

func (lr *LavaRequest) Validate() error {
	if lr.Repo != "go" && lr.Repo != "pip" && lr.Repo != "npm" {
		return fmt.Errorf("%s is not a valid repo", lr.Repo)
	}
	return nil
}
