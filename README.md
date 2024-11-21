# OnlineJudge-JSUT
## 序言

感谢使用 JSUT-OJ 后端 api, 本项目由江苏理工学院学生从 0 开始自主编写, 若您对该项目感兴趣, 不妨动动鼠标在右上角点一个 star 😊

## 项目简介

本项目使用 Python Flask 框架 + Postgresql 数据库编写的 api 后端, 仅通过 http 协议使用 json 与服务器交换数据, 真正意义上实现前后端分离.

目前实现了如下功能:

- 基本的用户管理, 包括登录, 注册, 权限管理等
- 创建题目, 上传输入输出测试点
- docker 沙箱化编译运行以防恶意代码
- celery 任务化异步运行判题减少因多人提交主线程阻塞

todo list

- [x] 创建比赛
- [ ] 删除题目, 删除或更改测试点信息

## 项目部署

这里以 Ubuntu 24.04 为例介绍搭建过程

### 安装 PostgreSQL

安装过程很简便, 首先更新一下软件包列表然后安装 PostgreSQL:

```shell
apt update
apt install postgresql
```

### 配置 PostgreSQL

首先是一些新安装后的初始工作.刚安装好 PostgreSQL 时会自动新创建一个数据库用户和一个 Linux 系统用户, 用户名都是 postgres, 用以作为超级管理员管理数据库.所以先更改一下这两个用户的密码.

```shell
su postgres #以postgres用户登录Linux系统
psql #进入数据库
```
然后命令行前面的提示符会变成 postgres=#.接下来通过以下将数据库用户 postgres 的密码更改为 example.

```sql
ALTER USER postgres WITH PASSWORD 'example';
```

注意在数据库内 `;` 才代表这句命令完全结束了. 若未完全结束, 前面的提示符会变成 `postgres-#`. 所以记得加上 `;`. 

然后使用 `\q` 退出数据库, 然后使用 `exit` 退出 postgres 用户回到 root 用户. 接着使用以下命令修改 Linux 系统用户 postgres 的密码.
```shell
passwd -d postgres #清除postgres用户的初始密码
su postgres #重新进入postgres用户
passwd #修改postgres用户的密码
```

下面建议创建一个新的用户避免使用 postgres 直接操作数据库, 因此我这里创建一个 JsutOJAdmin 用户:
```shell
createuser --pwprompt JsutOJAdmin
```
其中 --pwprompt 表示建立该用户时设置密码, 更详细的参数可参考 createuser . 

然后进入数据库
```shell
psql
```
然后创建一个数据库用来存放该项目, 我这里以数据库名 `JsutOJ` 为例:
```sql
CREATE DATABASE JsutOJ
ENCODING 'UTF8'
OWNER JsutOJAdmin;
```

接着来到 /etc/postgresql/<pg_version>/main/ 下修改配置文件 pg_hba.conf, 其中 pg_version 是你的 PostgreSQL 版本号. 若没有找到该路径或文件请使用 find / -name pg_hba.conf 命令找到 pg.hba.conf 文件在哪. pg_hba.conf 用于配置客户端对数据库进行认证的详细参数. 具体格式和内容可参考 pg_hba.conf文件. 这里按照我的需求在文件末尾新开一行添加以下内容：
```conf
host    JsutOJ      JsutOJAdmin     ::1/128     md5
```
每项参数含义如下：

1. host：允许 TCP/IP 连接, 不论是否使用 SSL. 
2. JsutOJ：只允许连接数据库 JsutOJ. 
3. JsutOJAdmin：只允许用户 JsutOJAdmin 连接此数据库. 
4. ::1/128：即 127.0.0.1/32. 
5. md5：使用 md5 加密密码. 若没有设置密码请将此项改为 trust. 

保存退出, 至此, PostgreSQL 的配置就彻底完成了.

### 拉取源码并初始化项目
(此后的步骤均可直接运行快速安装脚本)
#### 快速搭建
Ubuntu:
```shell
curl -fsSL https://raw.githubusercontent.com/2b-creator/OnlineJudge-JSUT/refs/heads/main/ubuntu-install.sh | bash
```

#### 手动搭建
运行命令:

```shell
git clone https://github.com/2b-creator/OnlineJudge-JSUT.git
cd ./OnlineJudge-JSUT
```
首先运行安装库:
```shell
pip3 install -r requirements.txt
```
安装完毕后初始化数据库:
```shell
python3 ./InitDatabase.py
```

### 安装 docker 判题环境
```shell
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
```
### 为 docker 添加非 root 运行
```shell
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker 
#查看所有容器
docker ps -a
groupadd -f docker
```
### 生成镜像
根据项目根目录的 Dockerfile 生成镜像:
```shell
docker build -t sandbox .
```
### 添加 redis 队列服务器
```shell
sudo apt install redis-server
```
### 启动 redis, celery, 主程序
```shell
# 下面三个后台分别启动, 或添加到 systemd 服务
redis-server
celery -A tasks worker --loglevel=info
gunicorn -w 4 main:app
```
由此完成了搭建流程, 下面是测试脚本
```shell
curl -X GET http://127.0.0.1:8000 
```
如果输出 `hello world`, 恭喜你搭建成功!

## 反向代理(可选)
(To Be Continued)