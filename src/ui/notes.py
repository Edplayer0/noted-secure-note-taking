import customtkinter as ctk
from mediator.app_mediator import AppMediator

app_mediator = AppMediator()


class Note(ctk.CTkFrame):
    def __init__(self, master, data: tuple, notes_count: int):
        super().__init__(master)

        self.data: tuple = data

        self.title: str = data[1]
        self.date: str = data[2]

        self.count = notes_count

        self.configure(fg_color="#dcdcdc")

        self.title_label = ctk.CTkLabel(
            self, text=self.title, font=ctk.CTkFont(family="Segoe Script", size=22)
        )
        self.title_label.pack(pady=20, padx=10)

        self.date_label = ctk.CTkLabel(
            self,
            text=self.date,
            font=ctk.CTkFont(family="Arial", size=17),
        )
        self.date_label.pack()

        self.edit_button = ctk.CTkButton(
            self,
            text="",
            width=20,
            fg_color="#FFEE8C",
            font=ctk.CTkFont(family="Segoe UI Symbol", size=20),
            command=lambda: app_mediator.call_event("open_editor", self.data),
            hover_color="gray",
            cursor="hand2",
            text_color="white",
            corner_radius=20,
        )
        self.edit_button.pack(padx=10, pady=10, side="bottom")

    def show(self):

        column = 0 if self.count % 2 == 0 else 1
        row = 0 if self.count < 2 else 1

        self.grid(column=column, row=row, sticky="nsew", pady=10, padx=10)
