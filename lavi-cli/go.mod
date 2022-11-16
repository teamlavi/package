module lavi

go 1.18

require dep-tree-gen v0.0.0 // WE NEED TO KEEP THESE LINES

require (
	github.com/google/uuid v1.3.0
	github.com/gorilla/mux v1.8.0
	github.com/jedib0t/go-pretty/v6 v6.4.2
	github.com/schollz/progressbar/v3 v3.12.1
	github.com/spf13/cobra v1.6.1
)

require (
	github.com/BurntSushi/toml v1.2.1 // indirect
	github.com/adrg/strutil v0.3.0 // indirect
	github.com/inconshreveable/mousetrap v1.0.1 // indirect
	github.com/mattn/go-runewidth v0.0.14 // indirect
	github.com/mitchellh/colorstring v0.0.0-20190213212951-d06e56a500db // indirect
	github.com/rivo/uniseg v0.4.2 // indirect
	github.com/spf13/pflag v1.0.5 // indirect
	golang.org/x/sys v0.2.0 // indirect
	golang.org/x/term v0.2.0 // indirect
)

replace dep-tree-gen v0.0.0 => ../dep-tree-gen // WE NEED TO KEEP THESE LINES
