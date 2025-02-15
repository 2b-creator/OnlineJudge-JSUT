# OnlineJudge-JSUT

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/2b-creator/OnlineJudge-JSUT) ![GitHub License](https://img.shields.io/github/license/2b-creator/OnlineJudge-JSUT) ![GitHub Repo stars](https://img.shields.io/github/stars/2b-creator/OnlineJudge-JSUT)
 

## 序言

感谢使用 JSUT-OJ 后端 api, 本项目由江苏理工学院学生从 0 开始自主编写, 若您对该项目感兴趣, 不妨动动鼠标在右上角点一个 star 😊

## 项目简介

本项目使用 Python Flask 框架 + Postgresql 数据库编写的 api 后端, 仅通过 http 协议使用 json 与服务器交换数据, 真正意义上实现前后端分离. 

[前端地址](https://github.com/2b-creator/JsutOJ-vue)

目前实现了如下功能:

- 基本的用户管理, 包括登录, 注册, 权限管理等
- 创建题目, 上传输入输出测试点
- docker 沙箱化编译运行以防恶意代码
- celery 任务化异步运行判题减少因多人提交主线程阻塞

todo list

- [ ] 创建比赛
- [ ] 删除题目, 删除或更改测试点信息

## 项目部署

详见[项目部署](./Docs/deploy.md)

## 使用文档

详见 [Api 文档](./Docs/api.md)

## 开发文档

(To Be Continued)