import base64

import pyDes

class PyDES3():
    des_key = '@_a7~Ul1l1!@lx100$#365#$'

    def __init__(self, key=''):
        """
        三重DES加密、对称加密。py2下不可用
        :param key: 密钥
        """
        self.key = key if key else PyDES3.des_key
        self.cryptor = pyDes.triple_des(self.key, padmode=pyDes.PAD_PKCS5)

    def encrypt(self, text):
        """
        加密
        :param text:
        :return:
        """
        x = self.cryptor.encrypt(text.encode())
        return base64.standard_b64encode(x).decode()

    def decrypt(self, text):
        """
        解密
        :param text:
        :return:
        """
        x = base64.standard_b64decode(text.encode())
        x = self.cryptor.decrypt(x)
        return x.decode()