from customtkinter import CTkButton, CTkFont


class NewButton(CTkButton):

    def __init__(self, master, app):
        super().__init__(master)

        self.configure(
            fg_color="transparent",
            text="+",
            font=CTkFont(family="Arial", size=30, weight="bold"),
            hover_color="gray",
            width=50,
            text_color="white",
            cursor="hand2",
            corner_radius=20,
            command=lambda: app.dashboard.editor.enter(),
        )
