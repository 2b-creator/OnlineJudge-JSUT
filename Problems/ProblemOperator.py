import os
import shutil
from flask import request
import psycopg2
from SerialToml import *
from pathlib import Path

from UserAdmin.Auth.GenJWT import get_username
from UserAdmin.UserLogic import get_user_id


def add_problems(title, problem_char_id, description, input_description, output_description, difficulty, time_limit, memory_limit, author_id, data_range_description) -> int:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO problems (title, problem_char_id, description, input_description, output_description, difficulty, time_limit, memory_limit, author_id, data_range_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (title, problem_char_id, description, input_description, output_description,
         difficulty, time_limit, memory_limit, author_id, data_range_description))
    problem_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return int(problem_id)


def get_question(start: int, num: int) -> dict[str, list]:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM problems WHERE is_public = TRUE ORDER BY id LIMIT %s OFFSET %s;",
                   (num, start))
    res = cursor.fetchall()
    ls = []
    for i in res:
        cursor.execute(
            "SELECT tags.tag_name FROM tags JOIN tag_problems ON tags.id = tag_problems.tag_id WHERE tag_problems.problem_id = %s", (i[0],))
        tag_name = cursor.fetchall()
        tag_name_list = []
        for j in range(len(tag_name)):
            tag_name_list.append(tag_name[j][0])
        dic = {"id": i[0], "title": i[1], "tag": tag_name_list}
        ls.append(dic)
    conn.close()
    return {"datas": ls}


def get_question_detail(problem_id: int) -> dict:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title, description, input_description, output_description, difficulty, time_limit, memory_limit, submit_count, ac_count FROM problems WHERE id = %s",
        (problem_id,))
    res = cursor.fetchall()[0]
    col = "title, description, input_description, output_description, difficulty, time_limit, memory_limit, submit_count, ac_count".split(
        ", ")
    # todo dic add sample
    dic = {key: res[i] for i, key in enumerate(col)}
    conn.close()
    return dic


def get_question_by_chars(problem_char_id: str) -> int:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM problems WHERE problem_char_id = %s", (problem_char_id,))
    res = cursor.fetchone()[0]
    conn.close()
    return int(res)


def get_question_char_by_id(problem_id: int) -> str:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT problem_char_id FROM problems WHERE id = %s", (problem_id,))
    res = cursor.fetchone()[0]
    conn.close()
    return res


def add_sample(problem_id: int, input: str, output: str, sample_description: str) -> None:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_samples (sample_in, sample_out, problem_id, sample_description) VALUES (%s, %s, %s, %s)",
                   (input, output, problem_id, sample_description))
    conn.commit()
    conn.close()


def submit_problem_zips(problem_root_path: Path) -> int:
    conf_file = problem_root_path/"config.toml"
    data_range_des = problem_root_path/"data_range.md"
    des = problem_root_path/"problem.md"
    in_file_des = problem_root_path/"input_description.md"
    out_file_des = problem_root_path/"output_description.md"
    with open(str(des), "r") as f:
        description = f.read()
    with open(str(in_file_des), "r") as f:
        input_description = f.read()
    with open(str(out_file_des), "r") as f:
        output_description = f.read()
    with open(str(conf_file), "r") as f:
        config = toml.load(f)
    with open(str(data_range_des), "r") as f:
        data_range_description = f.read()
    author_id = get_user_id(get_username(request.headers.get("access-token")))
    title = config["problem"]["title"]
    problem_char_id = config["problem"]["problem_char_id"]
    difficulty = config["problem"]["difficulty"]
    time_limit = config["limit"]["time"]
    memory_limit = config["limit"]["memory"]
    special_judge = config["special"]["judge"]
    special_score = config["special"]["score"]
    problem_id = add_problems(title, problem_char_id, description, input_description,
                              output_description, difficulty, time_limit, memory_limit, author_id, data_range_description)
    if not os.path.exists(f"./TestSamples/{problem_char_id}"):
        os.mkdir(f"./TestSamples/{problem_char_id}")  # todo
        os.mkdir(f"./TestSamples/{problem_char_id}/sandbox")

    test_folder = problem_root_path/"test"
    for files in test_folder.glob("*.in"):
        saves = f"{problem_char_id}-{files.stem}.in"
        shutil.copy(files, f"./TestSamples/{problem_char_id}/{saves}")
    for files in test_folder.glob("*.out"):
        saves = f"{problem_char_id}-{files.stem}.out"
        shutil.copy(files, f"./TestSamples/{problem_char_id}/{saves}")

    if special_judge == False:
        shutil.copy("./checker.cpp",
                    f"./TestSamples/{problem_char_id}/checker.cpp")

    if special_score == False:
        shutil.copy("./calc.py", f"./TestSamples/{problem_char_id}/calc.py")

    for file in (problem_root_path/"sample").glob("*.in"):
        file_name = files.stem
        with open(file, "r") as f:
            sample_in = f.read()
        out_file_name = problem_root_path/"sample"/f"{file_name}.out"
        with open(out_file_name, "r") as f:
            sample_out = f.read()
        sample_des_name = problem_root_path/"sample"/f"{file_name}.md"
        with open(sample_des_name, "r") as f:
            sample_description = f.read()
        add_sample(problem_id, sample_in, sample_out, sample_description)
    return problem_id
