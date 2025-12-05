from tkinter import Tk


class App(Tk):
    def __init__(self, app_mediator):
        super().__init__()

        self.mediator = app_mediator

        self.title("NotEd: Encrypted Note-Taking")
        self.geometry("450x500")
        self.config(bg="white")

        icon = self.mediator.call_event("files")["ICON"]

        self.iconbitmap(icon)

        self.mediator.add_handler("configure_cipher", self.configure_cipher)

    def configure_cipher(self, cipher):
        self.cipher = cipher
