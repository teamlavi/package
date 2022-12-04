package models

import (
	"fmt"
	"lava/internal/models/commands"

	"github.com/jedib0t/go-pretty/v6/text"
)

type TempLavaResponse struct {
	Status string      `json:"status"`
	Error  interface{} `json:"error"`
	Result interface{} `json:"result"`
}

type LavaResponse struct {
	Status string                        `json:"status"`
	Error  interface{}                   `json:"error"`
	Result commands.CommandResponseModel `json:"result"`
}

func statusToColor(status string) string {
	switch status {
	case "complete":
		return text.FgHiGreen.Sprint(status)
	case "pending":
		return text.FgHiYellow.Sprint(status)
	case "failure":
		return text.FgHiRed.Sprint(status)
	}
	return status
}

func (l LavaResponse) DisplayStatus() {
	fmt.Printf("Status: %s\n", statusToColor(l.Status))
}

func (l LavaResponse) Display() bool {
	l.DisplayStatus()
	if l.Result != nil {
		l.Result.Display()
		return true
	}
	return false
}

func (l LavaResponse) ToCSV() [][]string {
	return l.Result.ToCSV()
}
