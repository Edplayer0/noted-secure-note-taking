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
