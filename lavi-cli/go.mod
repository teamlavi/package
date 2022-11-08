module lavi

go 1.18

require dep-tree-gen v0.0.0 // WE NEED TO KEEP THESE LINES

require (
	github.com/google/uuid v1.3.0
	github.com/gorilla/mux v1.8.0
	github.com/spf13/cobra v1.6.1
)

require (
	github.com/BurntSushi/toml v1.2.1 // indirect
	github.com/cpuguy83/go-md2man/v2 v2.0.2 // indirect
	github.com/inconshreveable/mousetrap v1.0.1 // indirect
	github.com/russross/blackfriday/v2 v2.1.0 // indirect
	github.com/spf13/pflag v1.0.5 // indirect
	gopkg.in/check.v1 v0.0.0-20161208181325-20d25e280405 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
)

replace dep-tree-gen v0.0.0 => ../dep-tree-gen // WE NEED TO KEEP THESE LINES
