"""Cipher manager module."""

import base64

from cryptography.fernet import Fernet


class Cipher:
    """Cipher manager class.
    Manage the encryption and decryption of data.

    Args:
        app_mediator (Mediator): Application mediator.
    Methods:
        configure_cipher: Configure the cipher to use.
        encode: Encode data.
        decode: Decode data."""

    _initialized = False

    def __new__(cls) -> "Cipher":
        if not hasattr(cls, "_instance"):
            cls._instance = super(Cipher, cls).__new__(cls)
        return cls._instance

    def __init__(self):

        if self._initialized:
            return

        self._cipher: Fernet | None = None

    @property
    def cipher(self) -> Fernet | None:
        """Get the cipher."""
        return self._cipher

    def configure_cipher(self, cipher: Fernet) -> None:
        """Configure the cipher to use"""
        self._cipher = cipher

    def encode(self, info: str) -> str:
        """Encode the data"""

        encoded_info = base64.urlsafe_b64encode(
            self.cipher.encrypt(info.encode())
        ).decode()

        return encoded_info

    def decode(self, info: str) -> str:
        """Decode the data"""

        decoded_info = self.cipher.decrypt(base64.urlsafe_b64decode(info)).decode()

        return decoded_info
