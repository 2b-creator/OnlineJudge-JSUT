#!/bin/bash

git clone https://github.com/2b-creator/OnlineJudge-JSUT.git
cd ./OnlineJudge-JSUT || exit
root_dir=$(pwd)
pip3 install -r requirements.txt

#安装前先卸载操作系统默认安装的docker，
sudo apt-get remove docker docker-engine docker.io containerd runc
#安装必要支持
sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release
#添加 Docker 官方 GPG key （可能国内现在访问会存在问题）
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
# 阿里源（推荐使用阿里的gpg KEY）
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
#添加 apt 源:
#Docker官方源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
#阿里apt源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
#更新源
sudo apt update
sudo apt-get update
#安装最新版本的Docker
sudo apt install docker-ce docker-ce-cli containerd.io
#等待安装完成
#查看Docker版本
sudo docker version
#查看Docker运行状态
sudo systemctl status docker
sudo apt-get install bash-completion
sudo curl -L https://raw.githubusercontent.com/docker/docker-ce/master/components/cli/contrib/completion/bash/docker -o /etc/bash_completion.d/docker.sh
source /etc/bash_completion.d/docker.sh

sudo groupadd docker
sudo usermod -aG docker "$USER"
newgrp docker
#查看所有容器
docker ps -a
groupadd -f docker

echo "[Unit]
Description=The JustOJ Flask app
After=network.target

[Service]
Environment=\"$root_dir\"
ExecStart=gunicorn -w 4 main:app
WorkingDirectory=$root_dir
StandardOutput=journal
StandardError=journal
Restart=always
User=your_user
Group=your_group

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/oj_flask.service > /dev/null

echo "[Unit]
Description=The JustOJ celery tasks
After=network.target

[Service]
Environment=\"$root_dir\"
ExecStart=celery -A tasks worker --loglevel=info
WorkingDirectory=$root_dir
StandardOutput=journal
StandardError=journal
Restart=always
User=your_user
Group=your_group

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/tasks_celery.service > /dev/null
sudo apt install redis-server

sudo systemctl enable --now tasks_celery.service
sudo systemctl enable --now oj_flask.service
sudo systemctl enable --now redis

docker build -t sandbox .
