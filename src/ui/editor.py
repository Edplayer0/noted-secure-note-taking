"""Editor module for the NotEd application."""

import re
import tkinter as tk
from datetime import datetime
from typing import Optional
from customtkinter import CTkTextbox, CTkFont

from src.mediator.mediator import Mediator

from src.models.note_models import NoteData, NewNoteData, ModifyNoteData


class Editor(tk.Frame):
    """Note editor interface"""

    def __init__(self, master, app_mediator: Mediator):
        super().__init__(master)

        self.mediator = app_mediator

        self.app = master
        self.config(bg="white")

        self.current_note: Optional[int] = None

        # Entry para el título
        self.editor_entry = tk.Entry(
            self,
            font=("Segoe Script", 20),
            relief="flat",
            bg="white",
            highlightbackground="white",
            highlightthickness=0,
        )
        self.editor_entry.pack(fill="x", padx=10, pady=10)

        self.editor_text = CTkTextbox(
            self,
            pady=15,
            padx=15,
            font=CTkFont(family="Arial", size=20),
            wrap="word",
            fg_color="white",
        )
        self.editor_text.pack(fill="both", expand=True)

        self.mediator.add_handler("close_editor", self.exit, priority=1)
        self.mediator.add_handler("open_editor", self.enter, priority=5)
        self.mediator.add_handler("current_note", lambda: self.current_note)

    def enter(self, data: Optional[NoteData] = None) -> None:
        """Open the editor with a new note or an existing one"""

        def on_entry_focus_in(event):

            if self.editor_entry.get() == "Title...":
                self.editor_entry.delete(0, tk.END)
                self.editor_entry.config(fg="black")

        self.pack(fill="both", expand=True)

        if data is None:
            # Nueva nota
            self.editor_entry.config(fg="grey")
            self.editor_entry.insert(0, "Title...")
            self.editor_entry.bind("<FocusIn>", on_entry_focus_in)
            self.editor_text.focus_set()
            return

        # Editar nota existente
        self.current_note = data.id
        title: str = data.title
        date: str = data.date

        content = self.mediator.call_event("load_note_content", self.current_note)

        self.editor_entry.config(fg="black")
        self.editor_entry.insert(0, title)
        self.editor_text.insert("1.0", f"{date}\n{content}")

        self.update_idletasks()

        self.editor_text.focus_set()

    def save(self) -> None:
        """Save the current note being edited"""

        try:
            # El titulo actual
            current_title: str = self.editor_entry.get().strip()

            # El contenido de todo el campo de texto
            text_content: str = self.editor_text.get("1.0", "end-1c").strip()

            if not text_content or not current_title or current_title == "Title...":
                return

            current_date: str
            current_content: str

            # Si la longitud es menor a 10 se asume que no hay fecha
            if len(text_content) < 10:
                current_date = datetime.now().strftime("%d/%m/%Y")
                current_content = text_content

            else:
                file_date: str = self.editor_text.get("1.0", "end-1c").split("\n")[0]

                # Si la fecha no cumple el patron se genera una
                if not re.fullmatch(r"^\d\d/\d\d/\d\d\d\d$", file_date):
                    current_date = datetime.now().strftime("%d/%m/%Y")
                    current_content = self.editor_text.get("1.0", "end-1c")
                else:
                    current_date = file_date
                    current_content = self.editor_text.get(
                        "1.0", "end-1c"
                    ).removeprefix(current_date + "\n")

            if self.current_note is None:
                data = NewNoteData(
                    title=current_title,
                    content=current_content,
                    date=current_date,
                )

                self.mediator.call_event("add_note", data)
                return

            data = ModifyNoteData(
                id=self.current_note,
                title=current_title,
                date=current_date,
                content=current_content,
            )

            self.mediator.call_event("modify_note", data)

        except Exception as e:
            print(f"Error en guardado final: {e}")

    def exit(self, no_save=False) -> None:
        """Exit the editor, optionally saving the note"""

        if not no_save:
            self.save()

        # Limpiar la interfaz
        self.current_note = None
        self.editor_entry.delete(0, tk.END)

        self.editor_text.yview_moveto(0)
        self.editor_text.delete("1.0", tk.END)
        self.pack_forget()

        self.mediator.call_event("load_frames")
