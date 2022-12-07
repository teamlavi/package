#!/usr/bin/env bash

# Follow README.md to install

# Check if env var set
if [[ -z "${GH_ACCESS_TOKEN}" ]]
then
    echo "GH_ACCESS_TOKEN env var is not set"
    exit 1
fi

# Basic installs
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release postfix

# Install docker and its dependencies
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install golang
if ! [ -x "$(command -v go)" ]; then
  # Install go
  wget https://go.dev/dl/go1.19.4.linux-amd64.tar.gz
  tar -C /usr/local -xzf go1.19.4.linux-amd64.tar.gz
  export PATH=$PATH:/usr/local/go/bin
else
  echo "Go is already installed. Skipping installation."
fi

# Enable docker to start at boot
sudo systemctl enable docker
sudo systemctl start docker

# Add sync job to crontab
(sudo crontab -l 2>/dev/null; echo "*/5 * * * * PACKAGE_DIR=\"$(pwd)\" GH_ACCESS_TOKEN=\"${GH_ACCESS_TOKEN}\" API_PORT=80 bash \"$(pwd)/scripts/vm/sync.sh\"") | sudo crontab -
