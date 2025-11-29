import customtkinter as ctk


class Note(ctk.CTkFrame):
    def __init__(self, master, data, app, notes_count):
        super().__init__(master)

        self.count = notes_count

        self.configure(fg_color="#dcdcdc")

        self.id, self.title, self.content = data

        self.title_label = ctk.CTkLabel(
            self, text=self.title,
            font=ctk.CTkFont(family="Segoe Script", size=22))
        self.title_label.pack(pady=20, padx=10)

        self.date_label = ctk.CTkLabel(
            self, text=self.content[:10],
            font=ctk.CTkFont(family="Arial", size=17, underline=True)
        )
        self.date_label.pack()

        self.edit_button = ctk.CTkButton(
            self, text="->", width=20, fg_color="#FFEE8C",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            command=lambda data=data: app.dashboard.editor.enter(data=data),
            hover_color="gray", cursor="hand2", text_color="white",
            corner_radius=20)
        self.edit_button.pack(padx=10, pady=10, side="bottom")

    def show(self):

        column = 0 if self.count % 2 == 0 else 1
        row = 0 if self.count < 2 else 1

        self.grid(column=column, row=row, sticky="nsew", pady=10, padx=10)
