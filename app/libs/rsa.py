import base64

import rsa


class RsaKey:
    # 生成的密钥是Python对象
    public_key, private_key = rsa.newkeys(1024)

    # 转换为pem格式
    public_key_bytes = public_key.save_pkcs1()

    # pem格式解码、编码
    public_key_str = public_key_bytes.decode()
    encode_public_key_bytes = public_key_str.encode()

    # base64格式key
    public_key_base64 = base64.b64encode(public_key_str.encode()).decode()

    # 还原为Python对象
    # restore_public_key = rsa.PublicKey.load_pkcs1(public_key_bytes)
    restore_public_key = rsa.PublicKey.load_pkcs1(encode_public_key_bytes)

    @staticmethod
    def encrypt(msg):
        # 加密
        encrypted_msg = rsa.encrypt(msg.encode(), RsaKey.public_key)
        # base64成字符串
        encrypted_msg_str = base64.b64encode(encrypted_msg).decode()

        return encrypted_msg_str

    @staticmethod
    def decrypt(encrypted_msg_str):
        encrypted_msg = base64.b64decode(encrypted_msg_str.encode())
        msg = rsa.decrypt(encrypted_msg, RsaKey.private_key).decode()
        return msg

    # RSA 加密对被加密的内容（明文）是有长度限制的。
    # 因为最终的密文中会有11 bytes 的内容用来存放加密相关的元信息
    # 所以对于1024位的密钥来说，能加密的明文长度为: 1024 / 8 - 11 = 117 bytes
    # 如果要发送一段很长的字符串，就需要把字符串先转成 bytes 型数据，再按照117 bytes 一组拆分成很多组，对每一组分别加密。
    @staticmethod
    def encrypt_long_str(msg):
        msg_bytes = msg.encode()
        encrypted_msg = b''
        chunk_size = len(msg_bytes) // 117 + 1
        for chunk_index in range(chunk_size + 1):
            chunk = msg_bytes[chunk_index * 117: (chunk_index + 1) * 117]
            encrypted_msg += rsa.encrypt(chunk, RsaKey.public_key)
        encrypted_msg_str = base64.b64encode(encrypted_msg).decode()
        return encrypted_msg_str

    # 解密的时候，以密钥位数/8bytes一组先切分密文，再逐一解密，最后拼出明文的 bytes 型数据以后再.decode()转成字符串。
    @staticmethod
    def decrypt_long_str(encrypted_msg_str):
        encrypted_msg = base64.b64decode(encrypted_msg_str.encode())
        chunk_size = len(encrypted_msg) // 128
        msg_bytes = b''
        for chunk_index in range(chunk_size):
            chunk = encrypted_msg[chunk_index * 128: (chunk_index + 1) * 128]
            msg_bytes += rsa.decrypt(chunk, RsaKey.private_key)
        return msg_bytes.decode()


