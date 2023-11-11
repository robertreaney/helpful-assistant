#!/bin/bash
# setup
date +"%Y-%m-%d %H:%M:%S" > /startup-test-proof.log
sudo usermod -aG docker ubuntu

sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg git
# docker official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
# setup repo
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# update apt-get
sudo apt-get update
# install docker engine
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# install aws cli
sudo apt-get install -y awscli

mkdir ~/projects
cd ~/projects
git clone https://github.com/robertreaney/helpful-assistant.git
cd helpful-assistant

# launch application
# sudo docker compose -f ~/docker-compose.prod.yml up
sudo docker compose -f docker-compose.yml up --build -d --remove-orphans

