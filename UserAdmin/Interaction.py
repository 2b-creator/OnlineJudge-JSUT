import psycopg2
from SerialToml import *

def aget_detail_user_info(username: str) -> dict:
    conn = psycopg2.connect(database=database_name, user=database_username, password=database_password, host=addr,
                            port=port)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT users.nickname, users.ac_num, user_profiles.bio, user_profiles.avatar FROM users JOIN user_profiles ON users.id=user_profiles.user_id WHERE username = %s",
        (username,))
    res = cursor.fetchone()[0]
    try:
        dic = {"nickname": res[0], "ac_num": res[1], "bio": res[2], "avatar": res[3]}
        return dic
    except Exception as e:
        return {"data": "error"}
