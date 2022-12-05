package poll

import (
	"encoding/json"
	"fmt"
	"io"
	"lava/internal/files"
	"lava/internal/models"
	"lava/internal/models/commands"
	"log"
	"math/rand"
	"net/http"
	"os"
	"reflect"
	"time"
)

type Poller struct {
	id       string
	api      string
	dataType reflect.Type
	csvName  string
}

var letters = []rune("1234567890")

func randSeq(n int) string {
	rand.Seed(time.Now().Unix())
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

func New(id string, api string, dataType reflect.Type, csvName string) *Poller {
	return &Poller{
		id:       id,
		api:      api,
		dataType: dataType,
		csvName:  csvName,
	}
}

func (p *Poller) PollBlocking() {
	for {
		lr := p.poll()
		if lr.Status == "pending" {
			lr.DisplayStatus()
		} else {
			ok := lr.Display()
			if ok {
				csvData := lr.ToCSV()
				files.SaveCSV(p.csvName, csvData)
			}
			break
		}
		time.Sleep(1 * time.Second)
	}
}

func (p *Poller) poll() models.LavaResponse {
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

	resp, err := p.sendGet()
	if err != nil {
		panic("Get request to lava api failed")
	}

	body = p.extractBytes(resp)
	response := p.unmarshalToMap(body)
	lr := p.unmarshalMap(response, p.dataType)

	return lr
}

func (p *Poller) sendGet() (*http.Response, error) {
	resp, err := http.Get(fmt.Sprintf("%s?jobID=%s", p.api, p.id))

	return resp, err
}

// Reads body to byte array
func (p *Poller) extractBytes(resp *http.Response) []byte {
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		panic("failed to read api response")
	}
	return b
}

// // Convert bytes to map
func (c *Poller) unmarshalToMap(body []byte) map[string]interface{} {

	var res map[string]interface{}

	err := json.Unmarshal(body, &res)
	if err != nil {
		panic("Could not decode api response body")
	}

	return res
}

// // Convert map to models.LavaResponse
func (c *Poller) unmarshalMap(res map[string]interface{}, dataType reflect.Type) models.LavaResponse {

	if res["status"].(string) == "pending" || res["status"].(string) == "failure" {
		return models.LavaResponse{
			Status: res["status"].(string),
			Error:  res["error"],
			Result: nil,
		}
	}

	value := reflect.New(dataType).Interface().(commands.CommandResponseModel)

	valueBytes, err := json.Marshal(res["result"])
	if err != nil {
		panic("Could not decode api response body")

	}

	if err = json.Unmarshal(valueBytes, &value); err != nil {
		panic("Could not decode api response body")
	}

	out := models.LavaResponse{
		Status: res["status"].(string),
		Error:  res["error"],
		Result: value,
	}

	return out
}
