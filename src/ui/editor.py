"""Editor module for the NotEd application."""

import re
import tkinter as tk
from datetime import datetime
from typing import Optional
from customtkinter import CTkTextbox, CTkFont

from mediator.mediator import Mediator


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
            fg_color="white"
        )
        self.editor_text.pack(fill="both", expand=True)

        self.mediator.add_handler("close_editor", self.exit)
        self.mediator.add_handler("open_editor", self.enter)
        self.mediator.add_handler("current_note", lambda: self.current_note)

    def enter(self, data: tuple[int, str, str] | bool = None) -> None:
        """Open the editor with a new note or an existing one"""

        def on_entry_focus_in(event):

            if self.editor_entry.get() == "Título de la nota...":
                self.editor_entry.delete(0, tk.END)
                self.editor_entry.config(fg="black")

        self.pack(fill="both", expand=True)

        if data is None:
            # Nueva nota
            self.editor_entry.config(fg="grey")
            self.editor_entry.insert(0, "Título de la nota...")
            self.editor_entry.bind("<FocusIn>", on_entry_focus_in)
            self.editor_text.focus_set()
            return

        # Editar nota existente
        self.current_note = data[0]
        title: str = data[1]
        date: str = data[2]

        content = self.mediator.call_event("load_note_content", self.current_note)

        self.editor_entry.config(fg="black")
        self.editor_entry.insert(0, title)
        self.editor_text.insert("1.0", f"{date}\n{content}")

        self.editor_text.update()

        self.editor_text.focus_set()

    def save(self) -> None:
        """Save the current note being edited"""

        try:
            # El titulo actual
            current_title: str = self.editor_entry.get().strip()

            # El contenido de todo el campo de texto
            text_content: str = self.editor_text.get("1.0", "end-1c").strip()

            if not text_content or not current_title:
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
                    current_content = (
                        self.editor_text.get("1.0", "end-1c")
                    )
                else:
                    current_date = file_date
                    current_content = self.editor_text.get(
                        "1.0", "end-1c").removeprefix(current_date + "\n")

            if current_title and current_title != "Título de la nota...":

                if self.current_note is None:
                    data = (current_title, current_date, current_content)
                    self.mediator.call_event("add_note", data)
                    return

                data: tuple = (
                    self.current_note,
                    current_title,
                    current_date,
                    current_content,
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
