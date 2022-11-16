package client

import (
	"encoding/json"
	"fmt"
	"io"
	"lava/internal/models"
	"log"
	"net/http"
	"os"

	"github.com/spf13/cobra"
)

// going to be responsible for sending requests
type Client struct {
	remote string
}

// Variadic, but only the first value provided will be used
// Made it variadic so it can work with nothing provided
func New(remote ...string) *Client {
	useRemote := "https://lavi-lava.com/lavi"
	if len(remote) > 0 {
		useRemote = remote[0]
	}
	return &Client{
		remote: useRemote,
	}
}

/*
	ANY FUNCTION CALLED IN HERE MUST PANIC!!

	DO NOT USE LOG.FATAL
*/
func (c *Client) Run(cmd *cobra.Command, endpoint string) {
	var body []byte
	defer func() {
		if err := recover(); err != nil {
			fmt.Printf("LAVA failed. Error: %s\n", err)
			fmt.Println("Attempting to write api response body to a file for inspection and future use")
			if err := os.WriteFile(fmt.Sprintf("lava-response-%s.txt", randSeq(10)), body, 0644); err != nil {
				log.Fatal("Failed to write to file", err)
			}
			os.Exit(1)
		}
	}()
	request := models.BuildLavaRequest(cmd)
	resp, err := c.sendPost(request, endpoint)
	if err != nil {
		panic("Request to lava api failed")
	}

	body = c.extractBytes(resp)

	lavaResp := c.unmarshalBytes(body)
	lavaResp.Display(cmd.Name())
}

/*
	Sends the request to lava api.

	In the future, this will return a job id that will be picked up by another function
	to poll the get endpoint.
*/
func (c *Client) sendPost(body *models.LavaRequest, endpoint string) (*http.Response, error) {
	// TODO: THIS IS FOR POSTING WHEN THE API IS READY
	// json_data, err := json.Marshal(body)

	// if err != nil {
	// 	log.Fatal("unknown error occured while sending post request")
	// }

	// resp, err := http.Post(fmt.Sprintf("%s/%s", c.remote, endpoint), "application/json",
	// 	bytes.NewBuffer(json_data))

	// this jobID is included just so I can get a response from prod
	resp, err := http.Get(fmt.Sprintf("%s/%s?jobID=asdf", c.remote, endpoint))
	return resp, err
}

// Reads body to byte array
func (c *Client) extractBytes(resp *http.Response) []byte {
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		panic("failed to read api response")
	}
	return b
}

// Convert bytes to models.LavaResponse
func (c *Client) unmarshalBytes(body []byte) models.LavaResponse {

	var res models.LavaResponse

	err := json.Unmarshal(body, &res)
	if err != nil {
		panic("Could not decode api response body")
	}

	return res
}
