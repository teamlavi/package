package commands

type CommandResponseModel interface {
	Display()
	ToCSV() [][]string
}
