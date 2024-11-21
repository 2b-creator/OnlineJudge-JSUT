import psycopg2

from SerialToml import *


def create_competition(title: str, description: str, start_at: str, finish_at: str, sign_deter_time: str) -> int:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO competition (title, description, start_at, finish_at, sign_deter_time) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (title, description, start_at, finish_at, sign_deter_time))
    comp_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return int(comp_id)


def add_problem_for_competition(problem_ids: list[int], competition_id: int) -> list[int]:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    ls = []
    for i in problem_ids:
        cursor.execute("INSERT INTO problem_competition (problem_id, competition_id) VALUES (%s, %s) RETURNING id",
                       (i, competition_id))
        ls.append(int(cursor.fetchone()[0]))
    conn.commit()
    conn.close()
    return ls
