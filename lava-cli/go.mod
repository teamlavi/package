module lava

go 1.18

require dep-tree-gen v0.0.0 // WE NEED TO KEEP THESE LINES

require (
	github.com/jedib0t/go-pretty/v6 v6.4.2
	github.com/spf13/cobra v1.6.1
)

require (
	github.com/inconshreveable/mousetrap v1.0.1 // indirect
	github.com/mattn/go-runewidth v0.0.13 // indirect
	github.com/rivo/uniseg v0.2.0 // indirect
	github.com/spf13/pflag v1.0.5 // indirect
	github.com/stretchr/testify v1.8.1 // indirect
	golang.org/x/sys v0.0.0-20220908164124-27713097b956 // indirect
)

replace dep-tree-gen v0.0.0 => ../dep-tree-gen // WE NEED TO KEEP THESE LINES
