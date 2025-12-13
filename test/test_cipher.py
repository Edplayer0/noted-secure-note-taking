"""Tests for the Cipher class in the encryption manager."""

from cryptography.fernet import Fernet


def test_cipher_initialization(mocker):
    """Test the initialization of the Cipher class."""

    app_mediator = mocker.Mock()
    app_mediator.add_handler.return_value = None

    # Mock the Mediator class in the cipher module
    MockMediator = mocker.Mock()
    mocker.patch("src.managers.encryption.cipher.Mediator", MockMediator)

    from src.managers.encryption.cipher import Cipher

    cipher = Cipher(app_mediator)
    assert cipher is not None
    assert hasattr(cipher, "encode")
    assert hasattr(cipher, "decode")
    assert hasattr(cipher, "configure_cipher")


def test_cipher_encryption_decryption(mocker):
    """Test the encryption and decryption methods of the Cipher class."""

    app_mediator = mocker.Mock()
    app_mediator.add_handler.return_value = None

    fernet_cipher = Fernet(Fernet.generate_key())
    original_text = "This is a test string."

    # Mock the Mediator class in the cipher module
    MockMediator = mocker.Mock()
    mocker.patch("src.managers.encryption.cipher.Mediator", MockMediator)

    from src.managers.encryption.cipher import Cipher

    cipher = Cipher(app_mediator)
    cipher.configure_cipher(fernet_cipher)

    encrypted_text = cipher.encode(original_text)
    assert encrypted_text != original_text.encode()
    assert isinstance(encrypted_text, str)

    decrypted_text = cipher.decode(encrypted_text)
    assert decrypted_text == original_text
    assert isinstance(decrypted_text, str)
