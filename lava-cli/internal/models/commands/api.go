package commands

type CommandResponseModel interface {
	Display()
	Finalize()
}
