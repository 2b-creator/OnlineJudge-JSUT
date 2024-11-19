import jwt
from datetime import datetime, timedelta, UTC

SECRET_KEY = "jsut_oj"  # 替换为你的密钥


def generate_token(username):
    expiration = datetime.now(UTC) + timedelta(days=2)
    payload = {"username": username, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token, expiration


def validate_token(token, user_id):
    try:
        # 解码并验证令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload["username"] == user_id:
            return True
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
    return False


def get_username(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except jwt.ExpiredSignatureError:
        return 1
    except jwt.InvalidTokenError:
        return 2

