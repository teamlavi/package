package models

import (
	"log"
	"strings"
)

type Status string

var STATUS_PATCHED Status = "patched"
var STATUS_ACTIVE Status = "active"
var STATUS_ALL Status = "allVul"

func (s *Status) GetForValue(v string) Status {
	switch Status(strings.ToLower(v)) {
	case STATUS_PATCHED:
		return STATUS_PATCHED
	case STATUS_ACTIVE:
		return STATUS_ACTIVE
	case STATUS_ALL:
		return STATUS_ALL
	case Status("all"):
		return STATUS_ALL
	}
	return STATUS_ALL
}

type Level string

var LEVEL_DIRECT Level = "direct"
var LEVEL_INDIRECT Level = "indirect"
var LEVEL_BOTH Level = "both"

func (s *Level) GetForValue(v string) Level {
	switch Level(strings.ToLower(v)) {
	case LEVEL_DIRECT:
		return LEVEL_DIRECT
	case LEVEL_INDIRECT:
		return LEVEL_INDIRECT
	case LEVEL_BOTH:
		return LEVEL_BOTH
	case Level("all"):
		return LEVEL_BOTH
	}
	return LEVEL_BOTH
}

type Repo string

var REPO_PIP Repo = "pip"
var REPO_NPM Repo = "npm"
var REPO_GO Repo = "go"

func (s *Repo) GetForValue(v string) Repo {
	switch Repo(strings.ToLower(v)) {
	case REPO_PIP:
		return REPO_PIP
	case REPO_NPM:
		return REPO_NPM
	case REPO_GO:
		return REPO_GO
	}
	log.Fatalf("repository %s is not supported", v)
	return REPO_PIP
}
