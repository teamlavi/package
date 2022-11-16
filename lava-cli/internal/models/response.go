package models

import (
	"fmt"
	"lava/internal/models/commands"

	"github.com/jedib0t/go-pretty/v6/text"
)

type LavaResponse struct {
	Status string      `json:"status"`
	Error  interface{} `json:"error"`
	Result interface{} `json:"result"`
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

func (l LavaResponse) displayAndFinalizeByResult() {
	var data commands.CommandResponseModel
	switch l.Result.(type) {
	case commands.AffectedCountResponse:
		data = l.Result.(commands.AffectedCountResponse)
		break
	case commands.CountResponse:
		data = l.Result.(commands.CountResponse)
		break
	case commands.CountDepResponse:
		data = l.Result.(commands.CountDepResponse)
		break
	case commands.CountVulResponse:
		data = l.Result.(commands.CountVulResponse)
		break
	case commands.DepthResponse:
		data = l.Result.(commands.DepthResponse)
		break
	case commands.NumDownloadsResponse:
		data = l.Result.(commands.NumDownloadsResponse)
		break
	case commands.SeveritiesResponse:
		data = l.Result.(commands.SeveritiesResponse)
		break
	case commands.TypesResponse:
		data = l.Result.(commands.TypesResponse)
		break
	case commands.VulPackagesResponse:
		data = l.Result.(commands.VulPackagesResponse)
		break
	}
	data.Display()
	data.Finalize()
}

func (l LavaResponse) Display(queryName string) {
	fmt.Printf("Status: %s", statusToColor(l.Status))
	if l.Result != nil {
		l.displayAndFinalizeByResult()
	}
}
