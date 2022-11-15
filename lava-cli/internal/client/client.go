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

// ANY FUNCTION CALLED IN HERE MUST PANIC
// DO NOT USE LOG.FATAL
func (c *Client) Run(cmd *cobra.Command, endpoint string) {
	var resp *http.Response
	defer func() {
		if err := recover(); err != nil {
			fmt.Printf("LAVA failed. Error: %s\n", err)
			fmt.Println("Attempting to write api response body to a file for inspection and future use")
			out, err := os.Create(fmt.Sprintf("lava-response-%s.txt", randSeq(10)))
			if err != nil {
				fmt.Println(1, err)
				log.Fatal("Failed to create file")
			}
			defer out.Close()
			if _, err := io.Copy(out, resp.Body); err != nil {
				fmt.Println(2, err)
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
	lavaResp := c.handleResp(resp)
	fmt.Println(lavaResp)
}

// sends the request to lava api
// in the future, this will return a job id that will be picked up by another function
// to poll the get endpoint
func (c *Client) sendPost(body *models.LavaRequest, endpoint string) (*http.Response, error) {
	// TODO: THIS IS FOR POSTING WHEN THE API IS READY
	// json_data, err := json.Marshal(body)

	// if err != nil {
	// 	log.Fatal("unknown error occured while sending post request")
	// }

	// resp, err := http.Post(fmt.Sprintf("%s/%s", c.remote, endpoint), "application/json",
	// 	bytes.NewBuffer(json_data))

	resp, err := http.Get(fmt.Sprintf("%s/%s", c.remote, endpoint))
	return resp, err
}

// handles the response from the lava api
func (c *Client) handleResp(resp *http.Response) models.LavaResponse {

	var res models.LavaResponse

	err := json.NewDecoder(resp.Body).Decode(&res)
	fmt.Println(res, err)
	if err == nil {
		panic("Could not decode api response body")
	}

	return res
}
