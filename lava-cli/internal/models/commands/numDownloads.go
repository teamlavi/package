package commands

type NumDownloadsResponse struct {
	Downloads map[string]int `json:"downloads"` // Package id -> Number of package downloads
}

func (a NumDownloadsResponse) Display() {
	panic("not implemented") // TODO: Implement
}

func (a NumDownloadsResponse) ToCSV() [][]string {
	return [][]string{}
}
