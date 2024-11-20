# 基于官方的 GCC 镜像（包含 Linux 环境和基本工具）
FROM gcc:latest

# 安装 Python 和必要工具
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    time \
    && apt-get clean

# 添加非 root 用户以限制权限
RUN useradd -m sandbox_user
USER sandbox_user

# 工作目录（代码将在此目录中运行）
WORKDIR /sandbox