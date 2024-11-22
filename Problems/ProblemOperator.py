import psycopg2
from SerialToml import *


def add_problems(title, problem_char_id, description, input_description, output_description, sample_input,
                 sample_output,
                 difficulty, time_limit, memory_limit, author_id, tag) -> int:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO problems (title, problem_char_id, description, input_description, output_description, sample_input, sample_output, difficulty, time_limit, memory_limit, author_id, tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (title, problem_char_id, description, input_description, output_description, sample_input, sample_output,
         difficulty, time_limit, memory_limit, author_id, tag))
    problem_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return int(problem_id)


def get_question(start: int, num: int) -> dict[str, list]:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT (id, title, tag) FROM problems WHERE is_public = TRUE ORDER BY id LIMIT %s OFFSET %s;",
                   (num, start))
    res: list[tuple[str]] = cursor.fetchall()
    ls = []
    for i in res:
        tp = i[0][1:-1].split(",")
        dic = {"id": tp[0], "title": tp[1], "tag": tp[2]}
        ls.append(dic)
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
    return dic

