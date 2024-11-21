import psycopg2
from SerialToml import *
import UserAdmin.Auth.GenJWT


def login(username: str, password_hash_cm: str) -> dict:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
    password_hash = cursor.fetchone()[0]

    if password_hash is not None:
        if password_hash == password_hash_cm:
            cursor.execute("SELECT access_token FROM users WHERE username=%s", (username,))
            token = cursor.fetchone()[0]

            if token is None and UserAdmin.Auth.GenJWT.validate_token(token, username) == False:
                token = UserAdmin.Auth.GenJWT.generate_token(username)[0]
                cursor.execute("UPDATE users SET access-token = %s WHERE username=%s", (token, username))
                conn.commit()
            conn.close()
            return {"code": 200, "message": "login success", "access_token": token}
        conn.close()
        return {"code": 403, "message": "wrong password"}
    conn.close()
    return {"code": 404, "message": "no user found"}


def register(username: str, stu_id: int, password_hash_cm: str, email_cm: str):
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    access_token = UserAdmin.Auth.GenJWT.generate_token(username)
    cursor.execute(
        "INSERT INTO users (username, stu_id, password_hash, email, access_token) VALUES (%s, %s, %s, %s, %s)",
        (username, stu_id, password_hash_cm, email_cm, access_token))
    conn.commit()
    conn.close()
    return {"code": 200, "access-token": access_token, "message": "register success!"}


def check_role(username: str) -> str:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
    role = cursor.fetchone()[0]
    conn.close()
    return role


def change_role(username: str, role: str) -> None:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = %s WHERE username = %s", (role, username))
    conn.commit()
    conn.close()


def get_user_id(username: str) -> int:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()[0]
    return int(user_id)
