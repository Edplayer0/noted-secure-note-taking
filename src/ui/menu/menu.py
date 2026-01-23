"""Menu module for the NotEd application."""

from typing import Callable
from tkinter import Frame

import customtkinter as ctk

from src.mediator.mediator import Mediator
from src.ui.menu.register import Register


class Menu:
    """Menu class to manage the application menu."""

    def __init__(self, master, app_mediator: Mediator):
        self.mediator = app_mediator

        self.menu_frame = Frame(master)

        Register.config_menu(self)
        Register.load_functions()

        self.mediator.add_handler("show_menu", self.show)
        self.mediator.add_handler("exit_menu", self.exit)

    def exit(self):
        """Hide the menu."""
        self.menu_frame.pack_forget()

    def show(self):
        """Display the menu with registered functions."""
        self.menu_frame.pack(fill="both", expand=True)

    def add_button(self, label: str, function: Callable):
        """Add a button to the menu"""

        button = ctk.CTkButton(
            self.menu_frame,
            text=label,
            command=lambda: function(self.mediator),
            fg_color="#FFEE8C",
            hover_color="gray",
            font=ctk.CTkFont(family="Segoe UI Symbol", size=22, weight="bold"),
            text_color="white",
        )
        button.pack(pady=(10, 0), padx=10, fill="x", ipady=10, ipadx=10)
