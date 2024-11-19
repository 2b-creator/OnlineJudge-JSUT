import psycopg2


def add_submit_count(problem_id: int):
    conn = psycopg2.connect(database="JsutOJ", user="JsutOJAdmin", password="jsutojadmin", host="127.0.0.1",
                            port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT submit_count FROM problems WHERE problem_id=%s", (problem_id,))
    submit_count_get = int(cursor.fetchone()[0]) + 1
    cursor.execute("UPDATE problems SET submit_count = %s WHERE problem_id = %s", (submit_count_get, problem_id))
    conn.commit()
    conn.close()


def add_accept_count(problem_id: int):
    pass
