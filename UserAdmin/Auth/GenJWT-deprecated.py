import secrets
import time
import hashlib


def generate_access_token(user_id: str, secret_key: str, expiration_seconds: int = 3600):
    """
    生成一个访问令牌（access-token）

    :param user_id: 用户的唯一标识符
    :param secret_key: 用于签名令牌的密钥
    :param expiration_seconds: 令牌的有效时间（秒）
    :return: 包含令牌和到期时间的字典
    """
    # 获取当前时间戳
    timestamp = int(time.time())

    # 令牌到期时间
    expiration_time = timestamp + expiration_seconds

    # 随机部分
    random_token = secrets.token_hex(16)

    # 生成令牌的签名部分
    token_data = f"{user_id}:{expiration_time}:{random_token}"
    signature = hashlib.sha256((token_data + secret_key).encode()).hexdigest()

    # 拼接完整令牌
    access_token = f"{token_data}:{signature}"

    return {
        "access_token": access_token,
        "expires_at": expiration_time
    }


# 示例用法
if __name__ == "__main__":
    user_id = "123456"  # 假设用户ID
    secret_key = "my_secret_key"  # 用于签名的密钥
    token = generate_access_token(user_id, secret_key)

    print("Access Token:", token["access_token"])
    print("Expires At:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(token["expires_at"])))
