package client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"lava/internal/models"
	"lava/internal/poll"
	"log"
	"net/http"
	"os"
	"reflect"
	"strings"

	"github.com/spf13/cobra"
)

// going to be responsible for sending requests
type Client struct {
	allowNoRepo     bool
	remote          string
	api             string
	apiKey          string
	cmd             *cobra.Command
	responseType    reflect.Type
	requires        []models.Requires
	fillPkgsFromCve bool
}

func New() *Client {
	return &Client{}
}

func (c *Client) Cmd(cmd *cobra.Command) *Client {
	c.cmd = cmd
	return c
}

func (c *Client) FillPkgsFromCve() *Client {
	c.fillPkgsFromCve = true
	return c
}

func (c *Client) AllowNoRepo() *Client {
	c.allowNoRepo = true
	return c
}

func (c *Client) Api(api string) *Client {
	c.api = api
	return c
}

func (c *Client) ResponseType(dataType reflect.Type) *Client {
	c.responseType = dataType
	return c
}

func (c *Client) Requires(requires ...models.Requires) *Client {
	c.requires = requires
	return c
}

func (c *Client) remoteUrl() string {
	return fmt.Sprintf("%s/%s", c.remote, c.api)
}

func (c *Client) setApiKey() {
	apiKey, _ := c.cmd.Flags().GetString("api-key")
	if apiKey == "" {
		panic("api key must be provided")
	}
	c.apiKey = apiKey
}

func (c *Client) setRemote() {
	remote, _ := c.cmd.Flags().GetString("remote")
	if (strings.HasPrefix(remote, "http://") || strings.HasPrefix(remote, "https://")) && !strings.HasSuffix(remote, "/") {
		c.remote = remote
	} else {
		panic(fmt.Sprintf("remote url %s is invalid. Must start with http:// or https://, and not end with a slash", remote))
	}
}

/*
	ANY FUNCTION CALLED IN HERE MUST PANIC!!

	DO NOT USE LOG.FATAL
*/
func (c *Client) Run() {

	if c.cmd == nil {
		panic("error: need to provide cmd to the client")
	}

	if c.responseType == nil {
		panic("error: need to provide response type to the client")
	}

	var body []byte
	defer func() {
		if err := recover(); err != nil {
			fname := fmt.Sprintf("lava-response-%s.txt", randSeq(10))
			fmt.Printf("LAVA failed. Error: %s\n", err)
			fmt.Println("Attempting to write api response body to a file for inspection and future use. ", fname)
			if err := os.WriteFile((fname), body, 0644); err != nil {
				log.Fatal("Failed to write to file", err)
			}
			os.Exit(1)
		}
	}()
	c.setApiKey()
	c.setRemote()

	request, err := models.BuildLavaRequest(c.cmd, c.allowNoRepo, c.fillPkgsFromCve, c.requires...)
	fmt.Println(request)
	if err != nil {
		panic(err)
	}
	resp, err := c.sendPost(request)
	if err != nil {
		panic("Request to lava api failed")
	}

	body = c.extractBytes(resp)

	var res map[string]interface{}

	err = json.Unmarshal(body, &res)
	if err != nil {
		panic("Could not decode api response body")
	}

	id := res["result"].(string)

	csvName, _ := c.cmd.Flags().GetString("csv")
	// eventually need to include the auth code
	poller := poll.New(id, c.remoteUrl(), c.apiKey, c.responseType, csvName)
	poller.PollBlocking()
}

/*
	Sends the request to lava api.

	In the future, this will return a job id that will be picked up by another function
	to poll the get endpoint.
*/
func (c *Client) sendPost(body *models.LavaRequest) (*http.Response, error) {
	json_data, err := json.Marshal(body)

	if err != nil {
		panic("unknown error occured while sending post request")
	}

	req, err := http.NewRequest("POST", c.remoteUrl(), bytes.NewBuffer(json_data))
	if err != nil {
		panic("unknown error occured while sending post request")
	}

	client := &http.Client{}

	req.Header = http.Header{
		"Content-Type":  {"application/json"},
		"Authorization": {fmt.Sprintf("Bearer %s", c.apiKey)},
	}

	resp, err := client.Do(req)
	if err != nil {
		panic("unknown error occured while sending post request")
	}

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
