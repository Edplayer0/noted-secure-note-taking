import customtkinter as ctk

from tkinter import messagebox


class NewPassword(ctk.CTkToplevel):

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.title("Crear contraseña")

        self.geometry("300x200")

        self.after(250, lambda: self.iconbitmap(app.files["ICON"]))

        self.instruct = ctk.CTkLabel(
            self,
            text="Introduce la nueva contraseña",
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

        if self.entry1.get().strip() != self.entry2.get().strip():

            messagebox.showerror("Error", "Las contraseñas no coinciden")

            return

        self.app.password_manager.generate(self.entry1.get().strip())

        self.destroy()
