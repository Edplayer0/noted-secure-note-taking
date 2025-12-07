from functools import wraps
from typing import Callable
from tkinter import Frame

import customtkinter as ctk


class Menu:
    def __init__(self, master, app_mediator):
        self.mediator = app_mediator

        self.menu_frame = Frame(master)

        self.funcions: dict[str, Callable] = {}

        self.mediator.add_handler("show_menu", self.show)
        self.mediator.add_handler("exit_menu", self.exit)

    def registry_function(self, name: str, func: Callable) -> None:
        
        self.funcions[name] = func


    def exit(self):
        self.menu_frame.pack_forget()

    def show(self):
        self.menu_frame.pack(fill="both", expand=True)

        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        for name, func in self.funcions.items():
            button = ctk.CTkButton(
                self.menu_frame,
                text=name,
                command= lambda func=func: func(self.mediator),
                fg_color="#FFEE8C",
                hover_color="gray",
                font=ctk.CTkFont(family="Segoe UI Symbol", size=22),
                text_color="white",
            )
            button.pack(pady=10, padx=10, fill="x", ipady=10, ipadx=10)