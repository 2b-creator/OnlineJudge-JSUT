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
    cursor.execute("SELECT (title, tag) FROM problems WHERE is_public = TRUE ORDER BY id LIMIT %s OFFSET %s;",
                   (num, start))
    res = cursor.fetchall()
    ls = []
    for i in res:
        tp = tuple(i[0])
        dic = {"title": tp[0], "tag": tp[1]}
        ls.append(dic)
    return {"data": ls}
