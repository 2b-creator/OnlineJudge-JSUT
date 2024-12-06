import psycopg2
from SerialToml import *


def add_problems(title, problem_char_id, description, input_description, output_description, difficulty, time_limit,
                 memory_limit, author_id, tag) -> int:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO problems (title, problem_char_id, description, input_description, output_description, difficulty, time_limit, memory_limit, author_id, tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (title, problem_char_id, description, input_description, output_description,
         difficulty, time_limit, memory_limit, author_id, tag))
    problem_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return int(problem_id)


def get_question(start: int, num: int) -> dict[str, list]:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, tag FROM problems WHERE is_public = TRUE ORDER BY id LIMIT %s OFFSET %s;",
                   (num, start))
    res = cursor.fetchall()
    ls = []
    for i in res:
        dic = {"id": i[0], "title": i[1], "tag": i[2]}
        ls.append(dic)
    conn.close()
    return {"datas": ls}


def get_question_detail(problem_id: int) -> dict:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title, description, input_description, output_description, sample_input, sample_output, difficulty, tag, time_limit, memory_limit, submit_count, ac_count FROM problems WHERE id = %s",
        (problem_id,))
    res = cursor.fetchall()[0]
    col = "title, description, input_description, output_description, sample_input, sample_output, difficulty, tag, time_limit, memory_limit, submit_count, ac_count".split(
        ", ")
    dic = {key: res[i] for i, key in enumerate(col)}
    conn.close()
    return dic


def get_question_by_chars(problem_char_id: str) -> int:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM problems WHERE problem_char_id = %s", (problem_char_id,))
    res = cursor.fetchone()[0]
    conn.close()
    return int(res)


def get_question_char_by_id(problem_id: int) -> str:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT problem_char_id FROM problems WHERE id = %s", (problem_id,))
    res = cursor.fetchone()[0]
    conn.close()
    return res
