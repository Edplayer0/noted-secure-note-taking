from customtkinter import CTkFrame, set_appearance_mode
from ui.dashboard.notes.notes import Note
from mediator.mediator import Mediator

set_appearance_mode("light")


class NotesFrame(CTkFrame):

    def __init__(self, master, notes, app_mediator: Mediator):
        super().__init__(master)

        self.mediator = app_mediator

        self.frame = master

        self.notes = notes

        self.configure(fg_color="transparent")

        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(1, weight=1, uniform="group1")

    def show(self):

        self.pack(fill="both", expand=True)

        for note in self.winfo_children():
            note.destroy()

        notes_count = 0

        for note_data in self.notes:
            note = Note(self, note_data, notes_count, self.mediator)
            note.show()

            notes_count += 1

    def hide(self):

        self.pack_forget()
