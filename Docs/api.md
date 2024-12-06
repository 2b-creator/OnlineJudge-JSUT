## API 标准

JSUT-OJ 中客户端与服务器通信的基线是通过 HTTP API 交换 JSON 对象, 将来可能会指定更高效的传输作为可选扩展. 

建议使用 HTTPS 进行通信, 不建议在测试环境之外使用纯 HTTP. 

所有 `POST` 和 `PUT` 端点都要求客户端提供包含 `JSON` 对象（可能为空）的请求正文. 客户端应为所有包含 `JSON` 正文的请求提供 `application/json` 的 `Content-Type` 标头.

类似地, 所有端点都要求服务器返回 `JSON` 对象, 服务器必须为所有 `JSON` 响应包含 `application/json` 的 `Content-Type` 标头. 

某些客户端将被编写为在 Web 浏览器或类似环境中运行. 在这些情况下, 主服务器应响应预检请求并在所有请求上提供跨源资源共享 (CORS) 标头. 

服务器必须预期客户端将使用 OPTIONS 请求来接近它们, 从而允许客户端发现 CORS 标头. 本规范中的所有端点都支持 OPTIONS 方法, 但是, 当使用 OPTIONS 请求接近时, 服务器不得执行为端点定义的任何逻辑. 

当客户端使用请求服务器时, 服务器应使用该路由的 CORS 标头进行响应. 建议服务器在所有请求上返回的 CORS 标头为: 

```yaml
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: X-Requested-With, Content-Type, access-token
```

## 名词解释

### API 端点（API Endpoint）

API 端点（API Endpoint）是指应用程序编程接口（API）中提供服务的具体 URL 地址，它通常对应一个特定的资源或功能。每个 API 端点都表示一组可以通过 HTTP 请求进行交互的操作（如获取数据、提交数据、更新数据或删除数据）。

一个典型的 API 端点由以下几部分组成：

1. **协议**：通常是 `HTTP` 或 `HTTPS`，指定了与服务器的通信方式。
2. **域名或 IP 地址**：服务器的地址，告诉客户端请求发送到哪个服务器。
3. **路径**：API 的具体资源位置，通常代表一个具体的资源或操作。
4. **查询参数（可选）**：通过 URL 后面的 `?key=value` 形式传递的参数，用于进一步指定请求的细节。
5. **请求方法**：如 `GET`、`POST`、`PUT`、`DELETE` 等，指明对资源进行的操作类型。

例如：

```
GET https://api.example.com/users/123
```

- **协议**：`https`
- **域名**：`api.example.com`
- **路径**：`/users/123`（表示获取 ID 为 123 的用户信息）
- **请求方法**：`GET`（获取资源）

每个端点代表了 API 提供的一项具体功能。比如， `/users` 可能用于获取所有用户列表，而 `/users/123` 用于获取特定用户的详细信息。

### 数据库主键

数据库主键（Primary Key）是数据库表中的一个或多个字段的组合，用于唯一标识表中的每一行记录。主键的主要作用是确保表中的每一行数据都是唯一的，不会出现重复的记录。主键字段的值不能为 `NULL`，必须是唯一的，并且在表中每一行都必须有一个有效的主键值。

### 主键的特性：

1. **唯一性**：主键字段的值在表中必须是唯一的，不能重复。
2. **非空性**：主键字段的值不能为空，必须具有有效的值。
3. **稳定性**：主键值不应该被修改，因为主键通常用于关联其他表。

### 例如：

假设有一个 `学生` 表，表中包含 `学号`、`姓名`、`年龄` 等字段。如果选择 `学号` 作为主键，意味着每个学生都有一个唯一的学号，通过学号可以唯一标识每个学生。

| 学号 | 姓名 | 年龄 |
| ---- | ---- | ---- |
| 1001 | 张三 | 20   |
| 1002 | 李四 | 22   |
| 1003 | 王五 | 21   |

在这个例子中，`学号` 就是主键，它确保每个学生的学号是唯一且非空的；在本项目中我们可以通过主键的唯一性来查找某个数据，例如每一个问题都有一个唯一的 `problem_id` 与之对应。

## 注意事项

所有 api 端点会标出是否需要 `access-token` 标头, 即需要用户认证选项; 例如增加更改, 删除题目等操作, 需要用户在发送请求的时候附上该 `header` 字段. 同样在 `flask` 代码中, 在请求需要用户认证的 api 端点时, 使用 `@require_access_token` 装饰器进行验证. 

```python
def require_access_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取请求头中的 access-token
        access_token = request.headers.get('access-token')

        # 验证 access-token 是否存在以及是否有效
        if not access_token:
            return jsonify({"message": "Access token is missing"}), 401

        # 这里可以添加自己的逻辑来验证 token 是否有效
        # 比如, 假设有效的 token 为 "valid_token"
        if isinstance(get_username(access_token), int):
            return jsonify({"message": "Invalid access token"}), 403

        # 如果验证通过, 继续执行原始函数
        return f(*args, **kwargs)

    return decorated_function
```

## 端点一览

[GET 端点一览](./get.md)

[POST 端点一览](./post.md)