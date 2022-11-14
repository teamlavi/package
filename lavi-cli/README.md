# LAVI CLI

A command-line interface for LAVI's functionality.

# DOCKER

to build the docker image you need to be in the package folder because two different folders need to be copied into the build
```
dockber build -f lavi-cli/Dockerfile -t IMAGE:TAG .
```

# To Run or Build

Make sure you build the ui first
```
cd ui
npm i
npm run build
```

Then run or build the go code
```
# in the lavi-cli folder
go run main.go
```