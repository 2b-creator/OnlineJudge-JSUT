import psycopg2


def add_submit_count(problem_char_id: int) -> None:
    conn = psycopg2.connect(database="JsutOJ", user="JsutOJAdmin", password="jsutojadmin", host="127.0.0.1",
                            port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM problems WHERE problem_char_id = %s", (problem_char_id,))
    problem_id = cursor.fetchone()[0]
    cursor.execute("SELECT submit_count FROM problems WHERE id = %s", (problem_id,))
    submit_count_get = int(cursor.fetchone()[0]) + 1
    cursor.execute("UPDATE problems SET submit_count = %s WHERE problem_char_id = %s",
                   (submit_count_get, problem_char_id))
    conn.commit()
    conn.close()


'''
def add_accept_count(username: str, problem_id: int, language: str):
    conn = psycopg2.connect(database="JsutOJ", user="JsutOJAdmin", password="jsutojadmin", host="127.0.0.1",
                            port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT ac_count FROM problems WHERE problem_id = %s", (problem_id,))
    ac_count = int(cursor.fetchone()[0]) + 1
    cursor.execute("INSERT INTO user_problems (user_id, problem_id, ac_lang) VALUES (%s, %s, %s)",
                   (user_id, problem_id, language))
    cursor.execute("UPDATE problem SET ac_count = %s WHERE problem_id = %s", (ac_count, problem_id))
    conn.commit()
    conn.close()
'''
