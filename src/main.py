from app import App
from login import Login
from verifier import PasswordVerifier
from dashboard.dashboard import Dashboard
from functions.files import app_files
from managers.database_manager import DatabaseManager
from managers.password_manager import PasswordManager

# Archivos de la aplicacion
files = app_files()


def main():

    # Objeto de la aplicacion
    app = App(files, Login, PasswordVerifier,
              DatabaseManager, Dashboard, PasswordManager)

    # Muestra el login
    app.login.enter()

    # Loop de la aplicacion
    app.mainloop()


if __name__ == "__main__":

    main()
