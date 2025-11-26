from notes.notes import Note
from customtkinter import CTkFrame, set_appearance_mode

set_appearance_mode("light")


class NotesFrame(CTkFrame):

    def __init__(self, master, app, notes):
        super().__init__(master)

        self.frame = master

        self.app = app

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
            note = Note(self, note_data, self.app, notes_count)
            note.show()

            notes_count += 1

    def hide(self):

        self.pack_forget()
