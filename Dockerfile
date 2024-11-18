# 基于官方的 GCC 镜像
FROM gcc:latest

# 安装必要的工具
RUN apt-get update && apt-get install -y \
    time \
    && apt-get clean

# 添加非 root 用户以限制权限
RUN useradd -m sandbox_user
USER sandbox_user

# 工作目录
WORKDIR /sandbox

# 限制 CPU 和内存时长（可通过 Docker 运行参数限制）
