import base64

from mediator.app_mediator import AppMediator

app_mediator = AppMediator()


class Cipher:

    def __init__(self, cipher):

        self.cipher = cipher

        app_mediator.add_service(self)
        app_mediator.add_handler("encode", self.encode)
        app_mediator.add_handler("decode", self.decode)

    def encode(self, info: str):

        encoded_info = base64.urlsafe_b64encode(
            self.cipher.encrypt(info.encode())
        ).decode()

        return encoded_info

    def decode(self, info: str):

        decoded_info = self.cipher.decrypt(base64.urlsafe_b64decode(info)).decode()

        return decoded_info
