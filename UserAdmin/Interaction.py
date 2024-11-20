import psycopg2


def get_detail_user_info(username: str) -> dict:
    conn = psycopg2.connect(database="JsutOJ", user="JsutOJAdmin", password="jsutojadmin", host="127.0.0.1",
                            port="5432")
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
