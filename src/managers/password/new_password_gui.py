"""GUI for creating a new password."""

from tkinter import messagebox
import customtkinter as ctk

from src.mediator.mediator import Mediator


class NewPassword(ctk.CTkToplevel):
    """GUI for creating a new password."""

    def __init__(self, app_mediator: Mediator):
        super().__init__()

        self.mediator = app_mediator

        self.title("Creating a password")

        self.geometry("300x200")

        icon = app_mediator.call_event("files")["ICON"]

        self.after(250, lambda: self.iconbitmap(icon))

        self.instruct = ctk.CTkLabel(
            self,
            text="Introduce the new password",
            font=ctk.CTkFont(family="Arial", size=17, weight="bold"),
        )
        self.instruct.pack(pady=10)

        self.entry1 = ctk.CTkEntry(self)
        self.entry1.pack(pady=10)

        self.entry1.focus_set()

        self.entry2 = ctk.CTkEntry(self)
        self.entry2.pack()

        self.button = ctk.CTkButton(
            self,
            text="",
            command=self.generate,
            corner_radius=20,
            width=25,
            height=25,
            fg_color="#FFEE8C",
            text_color="white",
            hover_color="gray",
            font=ctk.CTkFont(family="Segoe UI Symbol", size=20),
        )
        self.button.pack(pady=10)

    def generate(self):
        """Generate the new password."""

        if self.entry1.get().strip() != self.entry2.get().strip():

            messagebox.showerror("Error", "The passwords aren't equal")

            return

        self.mediator.call_event("generate", self.entry1.get().strip())

        self.destroy()
