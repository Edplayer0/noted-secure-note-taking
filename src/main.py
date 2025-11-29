from app import App
from ui.login import Login
from ui.dashboard import Dashboard
from functions.files import app_files
from managers.database.database_manager import DatabaseManager
from managers.password.password_manager import PasswordManager

# Archivos de la aplicacion
files = app_files()


def main() -> None:

    # Objeto de la aplicacion
    app = App(files, Login, DatabaseManager, Dashboard, PasswordManager)

    # Muestra el login
    app.login.enter()

    # Loop de la aplicacion
    app.mainloop()


if __name__ == "__main__":

    main()
