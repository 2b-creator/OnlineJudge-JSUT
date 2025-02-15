from tasks import judge_work
from functools import wraps
import zipfile
import os.path
from pathlib import Path
from flask import Flask, request, jsonify

from Competitions.CompetitionOperator import create_competition
from Counters.CodeSubmitCounter import add_submit_count
from Counters.StatisticAccept import record_ac
from Problems.ProblemOperator import add_problems, get_question, get_question_detail, \
    get_question_char_by_id, add_sample, submit_problem_zips
from UserAdmin.Auth.GenJWT import get_username
from UserAdmin.Interaction import get_detail_user_info
from UserAdmin.UserLogic import *
import UserAdmin.UserLogic
import toml
from flask_cors import CORS
import shutil
app = Flask(__name__)
CORS(app)  # 允许所有来源的请求

tmp = 0
# 自定义装饰器


def require_access_token(func):
    @wraps(func)
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
        return func(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return "hello world"


@app.route('/api/version', methods=['GET'])
def get_version():
    return jsonify({"code": 200, "version": 1.0}), 200


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
    if "-" in username:
        return jsonify({"code": 401, "message": "'-' cannot in username!"}), 401
    stu_id = request.json.get("stu_id")
    password_hash_cm = request.json.get("password_hash_cm")
    email_cm = request.json.get("email_cm")
    info = UserAdmin.UserLogic.register(
        username, stu_id, password_hash_cm, email_cm)
    status_code = info["code"]
    return jsonify(info), status_code


@app.route('/api/submit', methods=['POST'])
@require_access_token
def submit_code():
    problem_id = request.json.get("id")
    username = get_username(request.headers.get("access-token"))
    code = request.json.get("code")
    language = request.json.get("language")
    dic = get_question_detail(problem_id)
    time_limit = dic["time_limit"]
    m_limit = dic["memory_limit"]
    problem_char_id = get_question_char_by_id(problem_id)
    task = judge_work.delay(problem_char_id, username,
                            code, language, time_limit)
    output = task.get()

    if task.failed():
        return jsonify({"code": 500, "message": f"Task failed with status: {task.status}"}), 500
    else:
        add_submit_count(problem_char_id)
        for i in output["results"]:
            if isinstance(i, str):
                break
            if i["status"] != "success":
                break
        else:
            record_ac(username, problem_char_id, language)
    return jsonify({"code": 200, "message:": "success!", "output": output}), 200


@app.route('/api/submit/cmp', methods=['POST'])
@require_access_token
def submit_competition():
    # todo
    problem_id = request.json.get("problem_id")
    cmp_id = request.json.get("competition_id")
    language = request.json.get("language")
    code = request.json.get("code")
    dic = get_question_detail(problem_id)
    time_limit = dic["time_limit"]
    m_limit = dic["memory_limit"]
    username = get_username(request.headers.get("access-token"))
    problem_char_id = get_question_char_by_id(problem_id)
    task = judge_work.delay(problem_char_id, username,
                            code, language, time_limit)
    output = task.get()
    if task.failed():
        return jsonify({"code": 500, "message": f"Task failed with status: {task.status}"}), 500
    else:
        add_submit_count(problem_char_id)
        for i in output["results"]:
            if isinstance(i, str):
                break
            if i["status"] != "success":
                break
        else:
            record_ac(username, problem_char_id, language)
    return jsonify({"code": 200, "message:": "success!", "output": output}), 200


@app.route('/api/add_problem', methods=['POST'])
@require_access_token
def add_problem():
    access_token = request.headers.get("access-token")
    if tmps := check_role(get_username(access_token)) != "admin":
        return jsonify({"code": 403, "message": "No privilege"}), 403
    upload_file = request.files.get("file")
    tmp = "upload"
    if not os.path.exists(f"./Temp"):
        os.mkdir("./Temp")
    upload_file.save(f"./Temp/{tmp}.tmp")
    try:
        with zipfile.ZipFile(f"./Temp/{tmp}.tmp", "r") as zip_ref:
            zip_ref.extractall(f"./Temp/{tmp}")
    except Exception as e:
        return jsonify({"code": 500, "message": f"Internal server error:{str(e)}"}), 500
    problem_ids: list[int] = []
    problem_root_path = Path(rf"./Temp/{tmp}")
    for folders in problem_root_path.glob("*[0-9]"):
        problem_id = submit_problem_zips(folders)
        problem_ids.append(problem_id)
    os.removedirs("./Temp")
    return jsonify({"code": 200, "problem_id": problem_ids}), 200


@app.route('/api/users', methods=['GET'])
def get_userinfo():
    username = request.args.get("username")
    data = get_detail_user_info(username)
    if data.get("data") is not None:
        return jsonify({"code": 200, "data": data}), 200
    return jsonify({"code": 404, "data": "user not found!"}), 404


@app.route('/api/create_competition', methods=['POST'])
@require_access_token
def add_competition():
    access_token = request.headers.get("access-token")
    if check_role(get_username(access_token)) != "admin":
        return jsonify({"code": 403, "message": "no privilege"}), 403
    title = request.json.get("title")
    description = request.json.get("description")
    start_at = request.json.get("start_at")
    finish_at = request.json.get("finish_at")
    sign_deter_time = request.json.get("sign_deter_time")
    try:
        create_competition(title, description, start_at,
                           finish_at, sign_deter_time)
        return jsonify({"code": 200, "message": "success"}), 200
    except Exception as e:
        return jsonify({"code": 500, "message": f"Internal server error: {str(e)}"}), 500


@app.route('/api/get_problems', methods=['GET'])
def get_problems():
    page = request.args.get("page")
    start = int(page) * 20 - 20
    dic = get_question(start, 20)
    return jsonify(dic), 200


@app.route('/api/get_problem_detail')
def get_problem_detail():
    problem_id = int(request.args.get("id"))
    dic = get_question_detail(problem_id)
    return jsonify({"code": 200, "data": dic}), 200


@app.route('/api/send_issue')
@require_access_token
def send_issue():
    content = request.args.get("content")  # todo


if __name__ == "__main__":
    app.run()
