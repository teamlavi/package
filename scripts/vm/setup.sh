#!/usr/bin/env bash

# Follow README.md to install

# Basic installs
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Install docker and its dependencies
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Enable docker to start at boot
sudo systemctl enable docker
sudo systemctl start docker

# Add sync job to crontab
(sudo crontab -l 2>/dev/null; echo "*/5 * * * * PACKAGE_DIR=\"$(pwd)\" \"$(pwd)/scripts/vm/sync.sh\"") | sudo crontab -
