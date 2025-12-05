from customtkinter import CTkButton, CTkFont

from mediator.mediator import Mediator


class NextButton(CTkButton):

    def __init__(self, master, app_mediator: Mediator):
        super().__init__(master)

        self.configure(
            fg_color="transparent",
            text=">",
            font=CTkFont(family="Arial", size=30, weight="bold"),
            hover_color="gray",
            width=50,
            text_color="white",
            cursor="hand2",
            corner_radius=20,
            command=lambda: app_mediator.call_event("next_frame"),
        )
