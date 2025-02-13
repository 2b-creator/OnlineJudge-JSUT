import psycopg2
from SerialToml import *

def record_ac(username: str, problem_char_id: str, language: str) -> None:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM problems WHERE problem_char_id = %s", (problem_char_id,))
    problem_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO user_problems (user_id, problem_id, ac_lang) VALUES (%s, %s, %s)",
                   (user_id, problem_id, language))
    cursor.execute("SELECT ac_count FROM problems WHERE id = %s", (problem_id,))
    ac_count = int(cursor.fetchone()[0]) + 1
    cursor.execute("UPDATE problems SET ac_count = %s WHERE id = %s", (ac_count, problem_id))
    conn.commit()
    conn.close()


def list_ac(username: str) -> list[int]:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT problem_id FROM user_problems WHERE user_id = %s", (user_id,))
    problem_ac_ls = list(cursor.fetchall()[0])
    return_ls = list(map(int, problem_ac_ls))
    return return_ls
