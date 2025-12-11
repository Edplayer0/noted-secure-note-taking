"""Main module of the NotEd application."""

import importlib
import pkgutil
from os.path import dirname
from ui.app import App
from ui.login import Login
from ui.dashboard.dashboard import Dashboard
from ui.menu.menu import Menu
from ui.menu import functions
from functions.files import app_files
from managers.database.database_manager import DatabaseManager
from managers.password.password_manager import PasswordManager
from managers.encryption.cipher import Cipher
from mediator.app_mediator import AppMediator

def load_menu_functions(menu: Menu):
    """Dynamically load and register menu functions."""

    # Get the path of the `functions` package
    functions_path = dirname(functions.__file__)

    # Discover all modules in the `functions` package
    for _, module_name, _ in pkgutil.iter_modules([functions_path]):
        module = importlib.import_module(f"ui.menu.functions.{module_name}")

        # Check for a `REGISTRY` dictionary in the module
        if hasattr(module, "REGISTRY"):
            for _, (label, func) in module.REGISTRY.items():
                menu.registry_function(label, func)

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

    # Dynamically load and register menu functions
    load_menu_functions(menu)

    # Manage the creation and verification of passwords
    PasswordManager(app_mediator)

    # Manage the encryption/decryption of notes
    Cipher(app_mediator)

    # Start the application showing the login
    app_mediator.call_event("show_login")

    # Call the mainloop of Tk
    app.mainloop()


if __name__ == "__main__":
    main()
