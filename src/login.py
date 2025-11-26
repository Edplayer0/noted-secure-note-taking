import tkinter as tk
from tkinter import ttk


class Login(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.header = tk.Label(self, fg="white", bg="#FFEE8C",
                               font=("Segoe Script", "35"), text="NotEd")
        self.header.pack(fill="x")

        self.login_box = tk.Frame(self, border=1, relief="solid")
        self.login_box.pack(fill="both", expand=True, pady=30, padx=35)

        self.saludo = tk.Label(self.login_box, text="\nBienvenido",
                               font=("Monotype Corsiva", "25"))
        self.saludo.pack()

        self.instruccion = tk.Label(
            self.login_box, text="\n\nIntroduce su contraseña:\n\n", font="Helvetica 15")
        self.instruccion.pack()

        self.entrada_contrasena = ttk.Entry(self.login_box, show="•")
        self.entrada_contrasena.pack()

        self.boton_login = ttk.Button(
            self.login_box, text="Enviar",
            command=lambda: master.password_manager.verify(
                bytearray(self.entrada_contrasena.get().encode())),
            state="disabled")
        self.boton_login.pack(pady=30)

        self.copylabel = tk.Label(
            self.login_box, text="EdgarProblem ©2025. Todos los derechos reservados.",
            font=("Arial", "8"), fg="gray")
        self.copylabel.pack(side="bottom")

    def enter(self):
        self.pack(fill="both", expand=True)

    def exit(self):
        self.destroy()
