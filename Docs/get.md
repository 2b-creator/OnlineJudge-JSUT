## GET /api/version

这个端点可以获取服务器的版本, 无特别请求体: 

### 响应体

| 字段    | 含义   |
| ------- | ------ |
| code    | 200    |
| version | 版本号 |

### `JSON` 示例

```json
{
    "code": 200,
    "version": "1.0"
}
```

## GET /api/get_problems

获取题库题目, 无特别请求体, 可指定参数 `page`, 默认 `page` 为获取数据库查询前 20 个题目:

### 响应体

包含一个 `JSON` 包括 `datas` 字段, `datas` 字段为一个列表. 

| 字段  | 含义                         |
| ----- | ---------------------------- |
| id    | 数据库题目序号, 为数据库主键 |
| title | 题目标题                     |
| tag   | 标签                         |

### `JSON` 示例

```json
{
    "datas": [
        {
            "id": 2,
            "title": "Hello JsutOJ",
            "tag": "测试"
        },
        {
            "id": 3,
            "title": "两数相加",
            "tag": "基础算法"
        }
    ]
}
```

## GET /api/get_problem_detail

根据 `problem_id` 获取题目详细信息，需要指定查询参数 `id`，例如:

```
GET	/api/get_problem_detail?id=1
```

### 响应体

| code | data                         |
| ---- | ---------------------------- |
| 200  | 字典, 表示问题的详细表示方法 |

data 字段体

| 字段               | 含义       |
| ------------------ | ---------- |
| title              | 题目的标题 |
| description        | 题目的描述 |
| input_description  | 输入描述   |
| output_description | 输出描述   |

### `JSON` 示例

```json
{
    "code": 200,
    "data": {
        "title": "两数相加",
        "description": "输入两个数, 空格隔开, 输出这两个整数的和",
        "input_description": "输入共一行, 两个用空格隔开的数字 $a$ $b$",
        "output_description": "输出一个数字 $c$, $c=a+b$, 保证数据范围 $c \in [-2^{31},2^{31}-1]$."
    }
}
```

需要注意的是, data 段中可能包含 latex 语法, 中途的反斜杠只需转义一次.

## GET /api/users

根据 `username` 获取用户详细信息，需要指定查询参数 `username`，例如:

```
GET	/api/get_problem_detail?username=dddsx
```

### 响应体

| code | data                         |
| ---- | ---------------------------- |
| 200  | 字典, 表示问题的详细表示方法 |

data 字段体

| 字段     | 含义     |
| -------- | -------- |
| nickname | 昵称     |
| ac_num   | ac数量   |
| bio      | 简介     |
| avatar   | 输出描述 |

### `JSON` 示例

```json
{
    "code": 200,
    "data": {
        "nickname": "孙笑川258",
        "ac_num": 258,
        "bio": "我这个人是非常儒雅随和的一个人",
        "avatar": "https://avatar.sunxiaochuan.com/avatars.png"
    }
}
```

