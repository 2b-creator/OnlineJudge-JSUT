## 注意事项

对于 `POST` 请求, 可能需要指定请求头和 `access-token` 登录令牌, 下面是使用 curl 与 requests 的例子:

### Shell: cURL

```shell
curl -X POST http://your-server.org:8000/api/add_problem \
-H "Content-Type: application/json" \
-H "access-token: your-access-token" \
-d '{
  "title": "等差数列求和",
  "problem_char_id": "addArithmeticSequence",
  "description": "这是 JSUT-OJ 的公式试机题, 给定一个等差数列 ${a_n}$, 其通项公式为 $a_n=cn+d,(c,d \\in \\mathbb{R},n \\in \\mathbb{Z^+})$, 求该数列的前 $n$ 项和. ",
  "input_description": "输入一行, 包括 $3$ 个整数 $c,d,n$. ",
  "output_description": "输出一个数字 $S$, 是为 ${a_n}$ 的前 $n$ 项的求和结果；输入数据保证输出数据在 $[-2^{31},2^{31}-1]$ 范围内. ",
  "difficulty": 1,
  "time_limit": 1,
  "memory_limit": 128
}'
```

### Python: requests

```python
import requests

url = "http://your-server.org:8000/api/add_problem"
headers = {
    "Content-Type": "application/json",
    "access-token": "your-access-token"
}
data = {
    "title": "等差数列求和",
    "problem_char_id": "addArithmeticSequence",
    "description": "这是 JSUT-OJ 的公式试机题, 给定一个等差数列 ${a_n}$, 其通项公式为 $a_n=cn+d,(c,d \\in \\mathbb{R},n \\in \\mathbb{Z^+})$, 求该数列的前 $n$ 项和. ",
    "input_description": "输入一行, 包括 $3$ 个整数 $c,d,n$. ",
    "output_description": "输出一个数字 $S$, 是为 ${a_n}$ 的前 $n$ 项的求和结果；输入数据保证输出数据在 $[-2^{31},2^{31}-1]$ 范围内. ",
    "difficulty": 1,
    "time_limit": 1,
    "memory_limit": 128
}

response = requests.post(url, headers=headers, json=data)

```

## 关于 `access-token`

利用 Python 的 pyjwt 库快速实现 JSON Web Token (JWT), 并作为 `access-token` 负载验证用户信息.

默认的 `access-token` 验证有效期为 2 天, 2 天后失效重新登录.

下面为生成代码:

```python
import jwt
from datetime import datetime, timedelta, UTC

SECRET_KEY = "jsut_oj"  # 替换为你的密钥


def generate_token(username):
    expiration = datetime.now(UTC) + timedelta(days=2)
    payload = {"username": username, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token, expiration


def validate_token(token, user_id):
    try:
        # 解码并验证令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload["username"] == user_id:
            return True
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
    finally:
        return False
```

## POST /api/register

注册用户并获取 `access-token` 登录凭据:

### 请求体

| 字段             | 含义                                                         |
| ---------------- | ------------------------------------------------------------ |
| username         | 用户名, 唯一的标识并用作登录的主要凭据                       |
| stu_id           | 学号, 一般是学校下发的学号, 适用于江苏理工学院学生. 可以作为登录的凭据 |
| password_hash_cm | 哈希运算后的密码, 通过约定的算法将密码加密存储于数据库中保证安全, 下面会给出加密代码 |
| email_cm         | 邮箱, 未来可用于密码找回与身份验证(施工中)                   |

对于密码的哈希加密, 下面给出相关加密算法:

- 后端加密 (Python)

```python
import hashlib
def md5_encrypt(input_strings: str) -> str:
    md5 = hashlib.md5()
    md5.update(input_strings.encode('utf-8'))
    return md5.hexdigest()
```

- 前端加密 (TypeScript)

```ts
import * as CryptoJS from 'crypto-js';
function md5_encrypt(input_strings: string): string {
    const hash = CryptoJS.MD5(input_strings);
    return hash.toString(CryptoJS.enc.Hex);
}
```

两个函数输入同样的字符均会返回相同的加密字符串.

### `JSON` 示例

```json
{
    "username": "SunXiaochuan258",
    "stu_id": "2024243108",
    "password_hash_cm": "6cd3556deb0da54bca060b4c39479839",
    "email_cm": "qjtykr65536@gmail.com"
}
```

### 响应体

| 字段         | 含义                                         |
| ------------ | -------------------------------------------- |
| code         | 响应代码                                     |
| message      | 信息                                         |
| access-token | 代码响应若为 200, 提供 access-token 登录令牌 |

### `JSON` 示例

错误响应 401

```json
{
    "code": 401,
    "message": "'-' cannot in username!"
}
```

正确响应 200

```json
{
    "code": 200,
    "access-token": "your-access-token",
    "message": "register success!"
}
```

## POST /api/login

为已经注册的用户验证获取 `access-token` 登录凭据:

### 请求体

| 字段             | 含义                                                         |
| ---------------- | ------------------------------------------------------------ |
| username         | 用户名, 登录的主要凭据                                       |
| password_hash_cm | 哈希运算后的密码, 通过约定的算法将密码加密存储于数据库中保证安全 |

### `JSON` 示例

```json
{
    "username": "SunXiaochuan258",
    "password_hash_cm": "6cd3556deb0da54bca060b4c39479839",
}
```

### 响应体

| 字段         | 含义                                         |
| ------------ | -------------------------------------------- |
| code         | 响应代码                                     |
| message      | 信息                                         |
| access-token | 代码响应若为 200, 提供 access-token 登录令牌 |

### `JSON` 示例

错误响应 403

```json
{
    "code": 403,
    "message": "wrong password"
}
```

错误响应 404

```json
{
    "code": 404,
    "message": "no user found"
}
```

正确响应 200

```json
{
    "code": 200,
    "message": "login success",
    "access_token": "your-access-token"
}
```

