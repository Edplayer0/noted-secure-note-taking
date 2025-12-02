import tkinter as tk
import customtkinter as ctk

from mediator.app_mediator import AppMediator

app_mediator = AppMediator()


class Login(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.header = tk.Label(
            self,
            fg="white",
            bg="#FFEE8C",
            font=ctk.CTkFont(family="Segoe Script", size=35),
            text="NotEd",
        )
        self.header.pack(fill="x")

        self.login_box = ctk.CTkFrame(self)
        self.login_box.pack(fill="both", expand=True, pady=30, padx=35)

        self.saludo = ctk.CTkLabel(
            self.login_box,
            text="\nBienvenido",
            font=ctk.CTkFont(family="Monotype Corsiva", size=33),
            padx=2,
            pady=2,
        )
        self.saludo.pack()

        self.instruccion = ctk.CTkLabel(
            self.login_box,
            text="\n\nIntroduce su contraseña:\n\n",
            font=ctk.CTkFont(family="Helvetica", size=20),
        )
        self.instruccion.pack()

        self.entrada_contrasena = ctk.CTkEntry(self.login_box, show="•")
        self.entrada_contrasena.pack()

        self.boton_login = ctk.CTkButton(
            self.login_box,
            text="",
            command=lambda: master.password_manager.verify(
                bytearray(self.entrada_contrasena.get().encode())
            ),
            state="disabled",
            fg_color="#FFEE8C",
            text_color="white",
            font=ctk.CTkFont(family="Segoe UI Symbol", size=20),
            hover_color="gray",
            width=20,
            corner_radius=20,
        )
        self.boton_login.pack(pady=30)

        self.copylabel = ctk.CTkLabel(
            self.login_box,
            text="© 2025 Edgar Ayuso Martínez. Released under the MIT Licence.",
            font=ctk.CTkFont(family="Arial", size=11),
        )
        self.copylabel.pack(side="bottom")

        app_mediator.add_handler("open_dashboard", self.exit)

    def enter(self):
        self.pack(fill="both", expand=True)

    def exit(self):
        self.destroy()
