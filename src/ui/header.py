import tkinter as tk
from functions.delete_note import delete_note
from mediator.app_mediator import AppMediator

app_mediator = AppMediator()


class Header(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.app = master

        self.current_mode = None

        self.config(bg="#FFEE8C")

        self.title = tk.Label(
            self,
            text="NotEd",
            bg="#FFEE8C",
            font=("Arial", 23, "bold"),
            pady=5,
            padx=15,
            fg="white",
        )
        self.menu_button = tk.Button(
            self,
            text="☰",
            bd=0,
            relief="flat",
            bg="#FFEE8C",
            fg="white",
            pady=5,
            padx=10,
            font="Arial 23",
            cursor="hand2",
        )
        self.back_button = tk.Button(
            self,
            text="<",
            bd=0,
            relief="flat",
            bg="#FFEE8C",
            fg="white",
            pady=5,
            padx=10,
            font="Arial 23",
            cursor="hand2",
            command=lambda: app_mediator.call_event("close_editor"),
        )
        self.delete_button = tk.Button(
            self,
            text="",
            bd=0,
            relief="flat",
            bg="#FFEE8C",
            fg="white",
            padx=10,
            font=("Segoe UI Symbol", 23),
            cursor="hand2",
            command=lambda: delete_note(master),
        )

        app_mediator.add_handler("close_editor", self.alter_mode)
        app_mediator.add_handler("open_editor", self.alter_mode)
        app_mediator.add_handler("open_dashboard", self.show)

    def show(self):

        if self.winfo_ismapped():
            return

        self.current_mode = "normal"

        self.title.pack(side="left")
        self.menu_button.pack(side="right")

        self.pack(fill="x")

    def alter_mode(self):

        if self.current_mode == "normal":

            self.title.pack_forget()
            self.menu_button.pack_forget()

            self.back_button.pack(side="left")
            self.delete_button.pack(side="right")

            self.current_mode = "editor"

        else:

            self.back_button.pack_forget()
            self.delete_button.pack_forget()

            self.title.pack(side="left")
            self.menu_button.pack(side="right")

            self.current_mode = "normal"
