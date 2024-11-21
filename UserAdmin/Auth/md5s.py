import hashlib


def md5_encrypt(input_strings: str) -> str:
    # 创建一个md5对象
    md5 = hashlib.md5()
    # 更新md5对象, 输入字符串需要先编码为字节
    md5.update(input_strings.encode('utf-8'))
    # 获取加密后的十六进制结果
    return md5.hexdigest()


if __name__ == "__main__":
    # 示例使用
    input_string = "Hello, world!"
    md5_hash = md5_encrypt(input_string)
    print("MD5 加密结果:", md5_hash)
