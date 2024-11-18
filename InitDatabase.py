import psycopg2

conn = psycopg2.connect(database="JsutOJ", user="JsutOJAdmin", password="jsutojadmin", host="127.0.0.1", port="5432")

# 首先对用户创建用户数据表

create_user_table = """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                -- 用户ID（自增主键）
    stu_id VARCHAR(50) UNIQUE NOT NULL,   -- 学号
    username VARCHAR(50) UNIQUE NOT NULL, -- 用户名
    nickname VARCHAR(50),                 -- 昵称，外显名称
    password_hash TEXT NOT NULL,          -- 密码（存储哈希值）
    email VARCHAR(100) UNIQUE NOT NULL,   -- 邮箱
    created_at TIMESTAMP DEFAULT NOW(),   -- 注册时间
    last_login TIMESTAMP,                 -- 最近登录时间
    role VARCHAR(20) DEFAULT 'user',      -- 角色（例如：user, admin, moderator）
    is_active BOOLEAN DEFAULT TRUE,       -- 账号是否激活
    ac_num int DEFAULT 0,                 -- ac 题目的数量
    access_token VARCHAR(100) UNIQUE NOT NULL      --登录时获取 access-token 令牌
);
"""
create_user_profiles = """
CREATE TABLE user_profiles (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE, -- 对应users表的id
    full_name VARCHAR(100),                -- 真实姓名
    bio TEXT,                              -- 简介
    avatar_url TEXT,                       -- 头像链接
    country VARCHAR(50),                   -- 国家
    language_preference VARCHAR(10)        -- 偏好语言
);
"""

create_user_statistics = """
CREATE TABLE user_statistics (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE, -- 对应users表的id
    problems_solved INT DEFAULT 0,          -- 解题数量
    submissions INT DEFAULT 0,              -- 提交数量
    accepted_rate FLOAT DEFAULT 0.0,        -- 通过率（Accepted / Submissions）
    rank INT DEFAULT 0                      -- 排名（可选：通过定期计算更新）
);
"""

create_permission = """
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,                  -- 权限ID
    name VARCHAR(50) UNIQUE NOT NULL,       -- 权限名称（例如：manage_users, view_reports）
    description TEXT                        -- 权限描述
);
"""

create_user_permissions = """
CREATE TABLE user_permissions (
    user_id INT REFERENCES users(id) ON DELETE CASCADE, -- 对应users表的id
    permission_id INT REFERENCES permissions(id) ON DELETE CASCADE, -- 对应permissions表的id
    PRIMARY KEY (user_id, permission_id)
);
"""

# 对题目创建题目数据表

create_question_data = """
CREATE TABLE problems (
    id SERIAL PRIMARY KEY,                  -- 题目ID（自增主键）
    title VARCHAR(255) NOT NULL,            -- 题目标题
    description TEXT NOT NULL,              -- 题目描述
    input_description TEXT NOT NULL,        -- 输入描述
    output_description TEXT NOT NULL,       -- 输出描述
    sample_input TEXT,                      -- 样例输入
    sample_output TEXT,                     -- 样例输出
    difficulty VARCHAR(20) DEFAULT 'easy',  -- 难度等级（easy, medium, hard）
    created_at TIMESTAMP DEFAULT NOW(),     -- 创建时间
    updated_at TIMESTAMP DEFAULT NOW(),     -- 更新时间
    time_limit INT NOT NULL,                -- 时间限制（单位：毫秒）
    memory_limit INT NOT NULL,              -- 内存限制（单位：MB）
    author_id INT REFERENCES users(id) ON DELETE SET NULL, -- 作者（可选）
    is_public BOOLEAN DEFAULT TRUE          -- 是否公开
);
"""

cursor = conn.cursor()
ls = [create_user_table, create_user_profiles, create_user_statistics, create_permission, create_user_permissions,
      create_question_data]
for i in ls:
    cursor.execute(i)
conn.commit()
conn.close()