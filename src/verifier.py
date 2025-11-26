import gc
import json
import base64

from tkinter import messagebox

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from managers.cipher import Cipher


class PasswordVerifier:

    def __init__(self, app):

        self.app = app

        self.password_file = app.files["PASSWORD_FILE"]

        with open(self.password_file, "r", encoding="UTF-8") as passw:
            self.password_data = json.load(passw)

        if self.password_data:

            self.truepass = base64.urlsafe_b64decode(self.password_data[0])
            self.salt1 = base64.urlsafe_b64decode(self.password_data[1])
            self.salt2 = base64.urlsafe_b64decode(self.password_data[2])

            self.app.login.boton_login.configure(state="normal")

        else:

            self.app.password_manager.new_password()

    def verify(self, user_pass):

        derivacion1 = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=self.salt1,
            iterations=200000
        )
        derivacion2 = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=self.salt2,
            iterations=200000
        )

        try:
            posible_pass = derivacion1.derive(bytes(user_pass))
            notas_pass = derivacion2.derive(bytes(user_pass))
        finally:
            for datos in enumerate(user_pass):
                index = datos[0]
                user_pass[index] = 0
            del user_pass
            gc.collect()

        if constant_time.bytes_eq(posible_pass, self.truepass):
            del posible_pass
            cipher = Fernet(base64.urlsafe_b64encode(notas_pass))
            del notas_pass
            self.app.cipher = Cipher(cipher)
            gc.collect()

            self.app.start()

        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
