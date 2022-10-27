module lavi-cli

go 1.18

require (
	github.com/inconshreveable/mousetrap v1.0.1 // indirect
	github.com/spf13/cobra v1.6.1 // indirect
	github.com/spf13/pflag v1.0.5 // indirect
	dep-tree-gen v0.0.0 // WE NEED TO KEEP THESE LINES
)

replace dep-tree-gen v0.0.0 => ../dep-tree-gen // WE NEED TO KEEP THESE LINES
