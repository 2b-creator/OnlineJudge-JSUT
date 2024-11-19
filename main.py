from crypt import methods

import celery
from flask import Flask, request
from pygments.lexers.jsonnet import jsonnet_token

from UserAdmin.Auth.GenJWT import validate_token, get_username
from UserAdmin.UserLogic import *
import UserAdmin.UserLogic

app = Flask(__name__)

from functools import wraps
from tasks import judge_work


# 自定义装饰器
def require_access_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 获取请求头中的 access-token
        access_token = request.headers.get('access-token')

        # 验证 access-token 是否存在以及是否有效
        if not access_token:
            return jsonify({"message": "Access token is missing"}), 401

        # 这里可以添加自己的逻辑来验证 token 是否有效
        # 比如，假设有效的 token 为 "valid_token"
        if isinstance(get_username(access_token), int):
            return jsonify({"message": "Invalid access token"}), 403

        # 如果验证通过，继续执行原始函数
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return "hello world"


@app.route('/api/login', methods=['POST'])
def user_login():
    username = request.json.get("username")
    password_hash = request.json.get("password_hash")
    info = UserAdmin.UserLogic.login(username, password_hash)
    return jsonify(info)


@app.route('/api/register', methods=['POST'])
def register_new():
    username = request.json.get("username")
    stu_id = request.json.get("stu_id")
    password_hash_cm = request.json.get("password_hash_cm")
    email_cm = request.json.get("email_cm")
    info = UserAdmin.UserLogic.register(username, stu_id, password_hash_cm, email_cm)
    return jsonify(info)


@app.route('/api/submit', methods=['POST'])
@require_access_token
def submit_code():
    problem_id = request.json.get("problem_id")
    username = get_username(request.headers.get("access-token"))
    code = request.json.get("code")
    language = request.json.get("language")
    task = judge_work.delay(problem_id, username, code, language)
    output = task.get()
    if task.failed():
        return jsonify({"code": 500, "message": f"Task failed with status: {task.status}"}), 500
    return jsonify({"code": 200, "message:": "success!"})


if __name__ == "__main__":
    app.run()
