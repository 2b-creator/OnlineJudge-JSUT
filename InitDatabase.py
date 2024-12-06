import psycopg2
import UserAdmin.UserLogic
from SerialToml import *
from UserAdmin.Auth.md5s import md5_encrypt

conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                        port=port)

# 首先对用户创建用户数据表

create_user_table = """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                -- 用户ID（自增主键）
    stu_id VARCHAR(50) UNIQUE NOT NULL,   -- 学号
    username VARCHAR(50) UNIQUE NOT NULL, -- 用户名
    nickname VARCHAR(50),                 -- 昵称, 外显名称
    password_hash TEXT NOT NULL,          -- 密码（存储哈希值）
    email VARCHAR(100) UNIQUE NOT NULL,   -- 邮箱
    created_at TIMESTAMP DEFAULT NOW(),   -- 注册时间
    last_login TIMESTAMP,                 -- 最近登录时间
    role VARCHAR(20) DEFAULT 'user',      -- 角色（例如：user, admin, moderator）
    is_active BOOLEAN DEFAULT TRUE,       -- 账号是否激活
    ac_num int DEFAULT 0,                 -- ac 题目的数量
    access_token TEXT UNIQUE NOT NULL      --登录时获取 access-token 令牌
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
    problem_char_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,            -- 题目标题
    description TEXT NOT NULL,              -- 题目描述
    input_description TEXT NOT NULL,        -- 输入描述
    output_description TEXT NOT NULL,       -- 输出描述
    difficulty INT DEFAULT 1,  -- 难度等级（easy, medium, hard）
    tag VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),     -- 创建时间
    updated_at TIMESTAMP DEFAULT NOW(),     -- 更新时间
    time_limit INT NOT NULL,                -- 时间限制（单位：毫秒）
    memory_limit INT NOT NULL,              -- 内存限制（单位：MB）
    submit_count INT NOT NULL DEFAULT 0,    -- 提交次数
    ac_count INT NOT NULL DEFAULT 0,        -- 通过次数
    author_id INT REFERENCES users(id) ON DELETE SET NULL, -- 作者（可选）
    is_public BOOLEAN DEFAULT TRUE          -- 是否公开
);
"""

# 关联表 users 和 ac 的 problems
join_user_ac_problems = """
CREATE TABLE user_problems (
    id SERIAL PRIMARY KEY, 
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    problem_id INT REFERENCES problems(id) ON DELETE CASCADE,
    ac_time TIMESTAMP DEFAULT NOW(),
    ac_lang VARCHAR(20) NOT NULL
);
"""

create_competition_table = """
CREATE TABLE competition (
    id SERIAL PRIMARY KEY,
    TITLE VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    strict_lang VARCHAR(20),
    sign_deter_time TIMESTAMP,
    start_at TIMESTAMP DEFAULT NOW(),
    finish_at TIMESTAMP
)
"""

create_user_competition = """
CREATE TABLE user_competition (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    competition_id INT REFERENCES competition(id) ON DELETE CASCADE,
    ac_list TEXT,
    submit_count INT NOT NULL DEFAULT 0,
    ac_count INT NOT NULL DEFAULT 0
)
"""

create_problem_competition = """
CREATE TABLE problem_competition (
    id SERIAL PRIMARY KEY,
    problem_id INT REFERENCES problems(id) ON DELETE CASCADE,
    competition_id INT REFERENCES competition(id) ON DELETE CASCADE
)
"""

sample_table = """
CREATE TABLE test_samples (
    id SERIAL PRIMARY KEY,
    sample_in TEXT,
    sample_out TEXT,
    problem_id INT REFERENCES problems(id) ON DELETE CASCADE
)
"""

cursor = conn.cursor()
ls = [create_user_table, create_user_profiles, create_user_statistics, create_permission, create_user_permissions,
      create_question_data, join_user_ac_problems, create_competition_table, create_user_competition,
      create_problem_competition]
for i in ls:
    cursor.execute(i)
    conn.commit()

# 加入 root 信息
password_hash = md5_encrypt(root_password)
UserAdmin.UserLogic.register(root_username, int(root_stu_id), password_hash, root_email)
UserAdmin.UserLogic.change_role(root_username, root_role)
conn.commit()
conn.close()
