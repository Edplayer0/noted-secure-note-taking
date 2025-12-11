"""Password Manager Module."""

import gc
import base64
import secrets

from tkinter import messagebox

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from managers.password.new_password_gui import NewPassword
from managers.password.key_manager import KeyManager


from mediator.mediator import Mediator


class PasswordManager:
    """Manages the creation and verification of user passwords.
    It uses PBKDF2HMAC for key derivation and Fernet for encryption/decryption.

    Attributes:
        mediator (Mediator): The application mediator for event handling.
        password_file (str): Path to the password file.
        key_manager (KeyManager): Manages key storage and retrieval.
        password_data (tuple): Loaded password data (truepass, salt1, salt2).
    Methods:
        verify(user_pass): Verifies the provided password.
        new_password(): Initiates the process to create a new password.
        generate(password): Generates and saves a new password.
    """

    def __init__(self, app_mediator: Mediator):

        self.mediator = app_mediator

        self.password_file = self.mediator.call_event("files")["PASSWORD_FILE"]

        self.key_manager = KeyManager(self.password_file)

        self.password_data = self.key_manager.load_keys()

        if self.password_data:

            self.truepass, self.salt1, self.salt2 = self.password_data

            self.mediator.call_event("enable_login_button")

        else:

            self.new_password()

        self.mediator.add_handler("verify_password", self.verify)
        self.mediator.add_handler("generate", self.generate)

    def verify(self, user_pass):
        """Verifies the provided password against the stored password."""

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

            self.mediator.call_event("configure_cipher", cipher)

            del notas_pass

            gc.collect()

            self.mediator.call_event("start")

        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    def new_password(self):
        """Initiates the process to create a new password."""

        NewPassword(self.mediator)

    def generate(self, password):
        """Generates and saves a new password."""

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

        self.mediator.call_event("enable_login_button")
