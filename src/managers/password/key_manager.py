import base64
import json


class KeyManager:
    def __init__(self, password_file):
        self.password_file = password_file

    def load_keys(self):
        with open(self.password_file, "r", encoding="UTF-8") as file:
            data = json.load(file)

        try:
            return (
                base64.urlsafe_b64decode(data[0]),
                base64.urlsafe_b64decode(data[1]),
                base64.urlsafe_b64decode(data[2]),
            )
        except IndexError:
            return False

    def save_keys(self, truepass, salt1, salt2):
        data = [
            base64.urlsafe_b64encode(truepass).decode("UTF-8"),
            base64.urlsafe_b64encode(salt1).decode("UTF-8"),
            base64.urlsafe_b64encode(salt2).decode("UTF-8"),
        ]
        with open(self.password_file, "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=4)
