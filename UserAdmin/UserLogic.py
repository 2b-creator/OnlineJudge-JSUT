import psycopg2
from flask import jsonify
import Auth.GenJWT


def login(username: str, password_hash_cm: str) -> dict:
    conn = psycopg2.connect(database="JsutOJ", user="JsutOJAdmin", password="jsutojadmin", host="127.0.0.1",
                            port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username='%s'", (username,))
    password_hash = cursor.fetchone()[0]

    if password_hash is not None:
        if password_hash == password_hash_cm:
            cursor.execute("SELECT access_token FROM users WHERE username=%s", (username,))
            token = cursor.fetchone()[0]

            if token is None and Auth.GenJWT.validate_token(token, username) == False:
                token = Auth.GenJWT.generate_token(username)[0]
                cursor.execute("UPDATE users SET access-token = %s WHERE username=%s", (token, username))
                conn.commit()
            conn.close()
            return {"code": 200, "message": "login success", "access_token": token}
        conn.close()
        return {"code": 403, "message": "wrong password"}
    conn.close()
    return {"code": 404, "message": "no user found"}


def register(username: str, stu_id: int, password_hash_cm: str, email_cm: str):
    conn = psycopg2.connect(database="JsutOJ", user="JsutOJAdmin", password="jsutojadmin", host="127.0.0.1",
                            port="5432")
    cursor = conn.cursor()
    access_token = Auth.GenJWT.generate_token(username)
    cursor.execute(
        "INSERT INTO users (username, stu_id, password_hash, email, access-token) VALUES (%s, %s, %s, %s, %s)",
        (username, stu_id, password_hash_cm, email_cm, access_token))
    conn.commit()
    conn.close()
    return {"code": 200, "access-token": access_token, "message": "register success!"}
