import customtkinter as ctk

from tkinter import messagebox


class NewPassword(ctk.CTkToplevel):

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.title("Crear contraseña")

        self.geometry("300x200")

        self.instruct = ctk.CTkLabel(
            self, text="Introduce la nueva contraseña")
        self.instruct.pack(pady=10)

        self.entry1 = ctk.CTkEntry(self)
        self.entry1.pack(pady=10)

        self.entry1.focus_set()

        self.entry2 = ctk.CTkEntry(self)
        self.entry2.pack()

        self.button = ctk.CTkButton(self, text="Crear", command=self.generate)
        self.button.pack(pady=10)

    def generate(self):

        if self.entry1.get().strip() != self.entry2.get().strip():

            messagebox.showerror("Error", "Las contraseñas no coinciden")

            return

        self.app.password_manager.generate(self.entry1.get().strip())

        self.destroy()
