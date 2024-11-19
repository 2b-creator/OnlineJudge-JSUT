import psycopg2


def add_problems(title, problem_char_id, description, input_description, output_description, sample_input, sample_output,
                difficulty, time_limit, memory_limit, author_id) -> int:
    conn = psycopg2.connect(database="JsutOJ", user="JsutOJAdmin", password="jsutojadmin", host="127.0.0.1",
                            port="5432")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO problems (title, problem_char_id, description, input_description, output_description, sample_input, sample_output, difficulty, time_limit, memory_limit, author_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (title, problem_char_id, description, input_description, output_description, sample_input, sample_output,
         difficulty, time_limit, memory_limit, author_id))
    problem_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return int(problem_id)
