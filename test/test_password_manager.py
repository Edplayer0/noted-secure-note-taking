"""Tests for the PasswordManager class."""

import os
import json


def test_password_manager(mocker):
    """Tests the PasswordManager class."""

    PASSWORD_FILE = "test/test_password.json"

    with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [],
            f,
            indent=4,
        )

    # Mock Cipher class
    Cipher = mocker.Mock()
    cipher_instance = mocker.Mock()
    Cipher.return_value = cipher_instance
    cipher_instance.configure_cipher.return_value = None

    # Mock Mediator
    app_mediator = mocker.Mock()
    app_mediator.call_event.return_value = {"PASSWORD_FILE": PASSWORD_FILE}
    app_mediator.add_handler.return_value = None

    # Mock NewPassword class
    mock_new_password = mocker.Mock()
    mock_new_password.return_value = None

    from src.managers.password.password_manager import PasswordManager

    # Mock tkinter messagebox
    mocker.patch("tkinter.messagebox.showerror", return_value=None)

    mocker.patch(
        "src.managers.password.password_manager.NewPassword", mock_new_password
    )
    mocker.patch("src.managers.password.password_manager.Cipher", Cipher)

    # Create PasswordManager instance
    password_manager = PasswordManager(app_mediator)

    # Assertions
    assert password_manager.mediator == app_mediator
    assert password_manager.password_file == PASSWORD_FILE
    assert hasattr(password_manager, "key_manager")
    assert hasattr(password_manager, "password_data")
    assert hasattr(password_manager, "new_password")
    assert hasattr(password_manager, "generate")
    assert hasattr(password_manager, "verify")

    mock_new_password.assert_called_once()

    password_manager.generate("testpassword")

    with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 3  # truepass, salt1, salt2

    assert password_manager.verify(bytearray("testpassword", encoding="utf-8")) is True

    assert (
        password_manager.verify(bytearray("wrongpassword", encoding="utf-8")) is False
    )

    os.remove(PASSWORD_FILE)
