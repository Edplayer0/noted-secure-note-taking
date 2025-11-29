import gc
import base64
import secrets

from tkinter import messagebox

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from managers.encryption.cipher import Cipher
from managers.password.new_password_gui import NewPassword
from managers.password.key_manager import KeyManager


class PasswordManager:

    def __init__(self, app):

        self.app = app

        self.password_file = self.app.files["PASSWORD_FILE"]

        self.key_manager = KeyManager(self.password_file)

        self.password_data = self.key_manager.load_keys()

        if self.password_data:

            self.truepass, self.salt1, self.salt2 = self.password_data

            self.app.login.boton_login.configure(state="normal")

        else:

            self.new_password()

    def verify(self, user_pass):

        derivacion1 = PBKDF2HMAC(
            algorithm=SHA256(), length=32, salt=self.salt1, iterations=200000
        )
        derivacion2 = PBKDF2HMAC(
            algorithm=SHA256(), length=32, salt=self.salt2, iterations=200000
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

    def new_password(self):

        new_pass = NewPassword(self.app)

    def generate(self, password):

        salt1 = secrets.token_bytes(16)
        salt2 = secrets.token_bytes(16)

        derivacion = PBKDF2HMAC(
            algorithm=SHA256(), length=32, salt=salt1, iterations=200000
        )

        new_pass = derivacion.derive(password.encode("UTF-8"))

        self.truepass = new_pass
        self.salt1 = salt1
        self.salt2 = salt2

        self.key_manager.save_keys(new_pass, salt1, salt2)

        self.app.login.boton_login.configure(state="normal")
