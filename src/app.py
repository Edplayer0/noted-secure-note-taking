from tkinter import Tk


class App(Tk):
    def __init__(self, files, Login, DatabaseManager, Dashboard, PasswordManager):
        super().__init__()

        self.title("NotEd: Notas de alta seguridad")
        self.geometry("450x500")
        self.config(bg="white")

        self.files = files

        self.iconbitmap(files["ICON"])

        self.database_manager = DatabaseManager(self)

        self.cipher = None

        self.login = Login(self)

        self.password_manager = PasswordManager(self)

        self.dashboard = Dashboard(self)

    def start(self):

        self.login.exit()

        self.dashboard.show()
