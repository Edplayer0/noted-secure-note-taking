from tkinter import Frame

from customtkinter import CTkFrame

from dashboard.footer.new_button import NewButton
from dashboard.footer.prev_button import PrevButton
from dashboard.footer.next_button import NextButton


class Footer(Frame):

    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")
        self.columnconfigure(2, weight=1, uniform="group1")
        self.columnconfigure(3, weight=1, uniform="group1")
        self.columnconfigure(4, weight=1, uniform="group1")

        self.inner_frame = CTkFrame(self, fg_color="#FFEE8C", corner_radius=20)

        self.inner_frame.columnconfigure(0, weight=1, uniform="group1")
        self.inner_frame.columnconfigure(1, weight=1, uniform="group1")
        self.inner_frame.columnconfigure(2, weight=1, uniform="group1")

        self.inner_frame.grid(column=1, row=0, sticky="nsew",
                              columnspan=3, pady=10, padx=10)

        self.new_button = NewButton(self.inner_frame, master)
        self.new_button.grid(column=1, row=0, sticky="nsew", pady=10, padx=10)

        self.prev_button = PrevButton(self.inner_frame, master)
        self.prev_button.grid(column=0, row=0, sticky="nsew", pady=10, padx=10)

        self.next_button = NextButton(self.inner_frame, master)
        self.next_button.grid(column=2, row=0, sticky="nsew", pady=10, padx=10)

    def show(self):

        self.pack(side="bottom", fill="x", ipady=10)

    def hide(self):

        self.pack_forget()
