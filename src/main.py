"""Main module of the NotEd application."""

from ui.app import App
from ui.login import Login
from ui.dashboard.dashboard import Dashboard
from ui.menu.menu import Menu
from ui.menu.functions import REGISTRY as MENU_FUNCTIONS
from functions.files import app_files
from managers.database.database_manager import DatabaseManager
from managers.password.password_manager import PasswordManager
from managers.encryption.cipher import Cipher
from mediator.app_mediator import AppMediator


def main() -> None:
    """Main function of the application."""

    # Services communications mediator
    app_mediator = AppMediator()

    # Makes available the file paths
    app_files(app_mediator)

    # Tkinter windows
    app = App(app_mediator)

    # Manage the database operations
    DatabaseManager(app_mediator)

    # UI
    Login(app, app_mediator)
    Dashboard(app, app_mediator)
    menu = Menu(app, app_mediator)

    # Register menu functions
    for name, func in MENU_FUNCTIONS.values():
        menu.registry_function(name, func)

    # Manage the creation and verification of passwords
    PasswordManager(app_mediator)

    # Manage the encription/decription of notes
    Cipher(app_mediator)

    # Start the aplication showing the login
    app_mediator.call_event("show_login")

    # Call the mainloop of Tk
    app.mainloop()


if __name__ == "__main__":

    main()
