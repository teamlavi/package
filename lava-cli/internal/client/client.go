package client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"lava/internal/models"
	"log"
	"net/http"

	"github.com/spf13/cobra"
)

// going to be responsible for sending requests
type Client struct {
	remote string
}

// variadic, but only the first value provided will be used
// made is variadic so it can work with nothing provided
func New(remote ...string) *Client {
	useRemote := "https://lavi-lava.com"
	if len(remote) > 0 {
		useRemote = remote[0]
	}
	return &Client{
		remote: useRemote,
	}
}

func (c *Client) Run(cmd *cobra.Command, endpoint string) {
	request := models.BuildLavaRequest(cmd)
	fmt.Println(request)
	c.sendPost(request, endpoint)
}

func (c *Client) sendPost(body *models.LavaRequest, endpoint string) (*http.Response, error) {
	json_data, err := json.Marshal(body)

	if err != nil {
		log.Fatal("unknown error occured while sending post request")
	}

	resp, err := http.Post(fmt.Sprintf("%s/%s", c.remote, endpoint), "application/json",
		bytes.NewBuffer(json_data))
	return resp, err
}
