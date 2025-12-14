"""Tests for the Cipher class in the encryption manager."""

from cryptography.fernet import Fernet


def test_cipher_initialization(mocker):
    """Test the initialization of the Cipher class."""

    from src.managers.encryption.cipher import Cipher

    cipher = Cipher()
    assert cipher is not None
    assert hasattr(cipher, "encode")
    assert hasattr(cipher, "decode")
    assert hasattr(cipher, "configure_cipher")

    fernet_cipher = Fernet(Fernet.generate_key())

    cipher.configure_cipher(fernet_cipher)

    assert cipher.cipher


def test_cipher_encryption_decryption(mocker):
    """Test the encryption and decryption methods of the Cipher class."""

    original_text = "This is a test string."

    from src.managers.encryption.cipher import Cipher

    cipher = Cipher()

    fernet_cipher = Fernet(Fernet.generate_key())

    cipher.configure_cipher(fernet_cipher)

    encrypted_text = cipher.encode(original_text)
    assert encrypted_text != original_text.encode()
    assert isinstance(encrypted_text, str)

    decrypted_text = cipher.decode(encrypted_text)
    assert decrypted_text == original_text
    assert isinstance(decrypted_text, str)
