from tkinter import Tk
from mediator.app_mediator import AppMediator

app_mediator = AppMediator()


class App(Tk):
    def __init__(self, files, Login, DatabaseManager, Dashboard, PasswordManager):
        super().__init__()

        self.title("NotEd: Encrypted Note-Taking")
        self.geometry("450x500")
        self.config(bg="white")

        self.files = files

        self.iconbitmap(files["ICON"])

        self.database_manager = DatabaseManager(self.files["DATABASE"])

        self.cipher = None

        self.login = Login(self)

        self.password_manager = PasswordManager(self)

        self.dashboard = Dashboard(self)

    def start(self) -> None:

        app_mediator.call_event("open_dashboard")
