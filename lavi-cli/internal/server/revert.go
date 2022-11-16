package server

import (
	"dep-tree-gen/common"
	"lavi/internal/config"
	"lavi/internal/repositories"
)

func RevertCommon(s config.ConfigInterface, cmdType string) string {
	if cmdType == common.PIP_CMD_NAME {
		pythonPath, _ := s.GetCmd().Flags().GetString("python")
		requirementsPath, _ := s.GetCmd().Flags().GetString("path")
		return repositories.PipRevert(s, pythonPath, requirementsPath)
	}
	if cmdType == common.GO_CMD_NAME {
		return repositories.GoRevert(s)
	}
	if cmdType == common.NPM_CMD_NAME {
		return repositories.NpmRevert(s)
	}
	if cmdType == common.POETRY_CMD_NAME {
		return repositories.PoetryRevert(s)
	}
	return ""
}
