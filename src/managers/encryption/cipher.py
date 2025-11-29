import base64


class Cipher:

    def __init__(self, cipher):

        self.cipher = cipher

    def encode(self, info):

        encoded_info = base64.urlsafe_b64encode(
            self.cipher.encrypt(info.encode())).decode()

        return encoded_info

    def decode(self, info):

        decoded_info = self.cipher.decrypt(
            base64.urlsafe_b64decode(info)).decode()

        return decoded_info
