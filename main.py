from flask import Flask, request

from Counters.CodeSubmitCounter import add_submit_count
from Counters.StatisticAccept import record_ac
from Problems.ProblemOperator import add_problems
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
    status_code = info["code"]
    return jsonify(info), status_code


@app.route('/api/register', methods=['POST'])
def register_new():
    username = request.json.get("username")
    stu_id = request.json.get("stu_id")
    password_hash_cm = request.json.get("password_hash_cm")
    email_cm = request.json.get("email_cm")
    info = UserAdmin.UserLogic.register(username, stu_id, password_hash_cm, email_cm)
    status_code = info["code"]
    return jsonify(info), status_code


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
    else:
        for i in output["results"]:
            if i["status"] != "success":
                add_submit_count(problem_id)
                break
        else:
            record_ac(username, problem_id, language)
    return jsonify({"code": 200, "message:": "success!", "output": output}), 200


@app.route('/api/add_problem', methods=['POST'])
@require_access_token
def add_problem():
    access_token = request.headers.get("access-token")
    if check_role(get_username(access_token)) != "user":
        return jsonify({"code": 403, "message": "no privilege"}), 403
    title = request.json.get("title")
    problem_char_id = request.json.get("problem_char_id")
    description = request.json.get("description")
    input_description = request.json.get("input_description")
    output_description = request.json.get("output_description")
    sample_input = request.json.get("sample_input")
    sample_output = request.json.get("sample_output")
    difficulty = request.json.get("difficulty")
    time_limit = request.json.get("time_limit")
    memory_limit = request.json.get("memory_limit")
    author_id = get_user_id(get_username(request.headers.get("access-token")))
    problem_id = add_problems(title, problem_char_id, description, input_description, output_description, sample_input,
                              sample_output, difficulty, time_limit, memory_limit, author_id)
    return jsonify({"code": 200, "problem_id": problem_id}), 200


if __name__ == "__main__":
    app.run()
