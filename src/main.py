"""Main module of the NotEd application."""

from src.ui.app import App
from src.ui.login import Login
from src.ui.dashboard.dashboard import Dashboard
from src.ui.menu.menu import Menu
from src.functions.files import app_files
from src.managers.database.database_manager import DatabaseManager
from src.managers.password.password_manager import PasswordManager
from src.mediator.app_mediator import AppMediator


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
    Menu(app, app_mediator)

    # Manage the creation and verification of passwords
    PasswordManager(app_mediator)

    # Start the application showing the login
    app_mediator.call_event("show_login")

    # Call the mainloop of Tk
    app.mainloop()


if __name__ == "__main__":
    main()
