from tkinter import Frame

from customtkinter import CTkFrame

from src.ui.dashboard.footer.new_button import NewButton
from src.ui.dashboard.footer.prev_button import PrevButton
from src.ui.dashboard.footer.next_button import NextButton

from src.mediator.mediator import Mediator


class Footer(Frame):

    def __init__(self, master, app_mediator: Mediator):
        super().__init__(master)

        self.mediator = app_mediator

        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")
        self.columnconfigure(2, weight=1, uniform="group1")
        self.columnconfigure(3, weight=1, uniform="group1")
        self.columnconfigure(4, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.inner_frame = CTkFrame(self, fg_color="#FFEE8C", corner_radius=20)

        self.inner_frame.columnconfigure(0, weight=1, uniform="group1")
        self.inner_frame.columnconfigure(1, weight=1, uniform="group1")
        self.inner_frame.columnconfigure(2, weight=1, uniform="group1")

        self.inner_frame.grid(column=1, row=1, sticky="ew", columnspan=3, padx=10)

        self.new_button = NewButton(self.inner_frame, app_mediator)
        self.new_button.grid(column=1, row=0, sticky="nsew", pady=10, padx=10)

        self.prev_button = PrevButton(self.inner_frame, app_mediator)
        self.prev_button.grid(column=0, row=0, sticky="nsew", pady=10, padx=10)

        self.next_button = NextButton(self.inner_frame, app_mediator)
        self.next_button.grid(column=2, row=0, sticky="nsew", pady=10, padx=10)

        self.mediator.add_handler("show_menu", self.hide)
        self.mediator.add_handler("exit_menu", self.show)
        self.mediator.add_handler("open_editor", self.hide)
        self.mediator.add_handler("close_editor", self.show)
        self.mediator.add_handler("start", self.show)

    def show(self):

        self.pack(side="bottom", fill="x", ipady=10)

    def hide(self):

        self.pack_forget()
