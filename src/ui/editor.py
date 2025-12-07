import re
import tkinter as tk
from datetime import datetime
from customtkinter import CTkScrollbar

from mediator.mediator import Mediator


class Editor(tk.Frame):
    """Editor de las notas"""

    def __init__(self, master, app_mediator: Mediator):
        super().__init__(master)

        self.mediator = app_mediator

        self.app = master
        self.config(bg="white")

        self.current_note: int | bool = False

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

        # Frame para el área de texto con scroll
        self.editor_text_frame = tk.Frame(self)
        self.editor_text_frame.columnconfigure(0, weight=1)
        self.editor_text_frame.rowconfigure(0, weight=1)
        self.editor_text_frame.pack(fill="both", expand=True)

        self.editor_text = tk.Text(
            self.editor_text_frame,
            pady=20,
            padx=20,
            font=("Arial", 15),
            border=0,
            wrap="word",
        )
        self.editor_text.grid(column=0, row=0, sticky="nsew")

        self.scroll = CTkScrollbar(
            self.editor_text_frame, command=self.editor_text.yview, bg_color="white"
        )
        self.scroll.grid(column=1, row=0, sticky="ns")
        self.editor_text.configure(yscrollcommand=self.scroll.set)

        self.mediator.add_handler("close_editor", self.exit)
        self.mediator.add_handler("open_editor", self.enter)
        self.mediator.add_handler("current_note", lambda: self.current_note)

    def enter(self, data: tuple[int, str, str] | bool = False) -> None:
        """Mostrar el editor y preparar para edición"""

        def on_entry_focus_in(event):
            if self.editor_entry.get() == "Título de la nota...":
                self.editor_entry.delete(0, tk.END)
                self.editor_entry.config(fg="black")

        self.pack(fill="both", expand=True)

        # Limpiar contenido previo
        self.editor_entry.delete(0, tk.END)
        self.editor_text.delete("1.0", tk.END)

        if not data:
            # Nueva nota
            self.current_note = False
            self.editor_entry.config(fg="grey")
            self.editor_entry.insert(0, "Título de la nota...")
            self.editor_entry.bind("<FocusIn>", on_entry_focus_in)
        else:
            # Editar nota existente
            self.current_note = data[0]
            title: str = data[1]
            date: str = data[2]

            content = self.mediator.call_event("load_note_content", self.current_note)

            self.editor_entry.config(fg="black")
            self.editor_entry.insert(0, title)
            self.editor_text.insert("1.0", date + content)

            self.update_idletasks()

        self.editor_text.focus_set()

    def save(self) -> None:
        """Guardar cambios"""
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
                current_content = "\n" + text_content

            else:
                possible_date: str = self.editor_text.get("1.0", "end-1c").strip()[:10]

                # Si la fecha no cumple el patron se genera una
                if not re.fullmatch(r"^\d\d/\d\d/\d\d\d\d$", possible_date):
                    current_date = datetime.now().strftime("%d/%m/%Y")
                    current_content = (
                        "\n" + self.editor_text.get("1.0", "end-1c").rstrip()
                    )
                else:
                    current_date = possible_date
                    current_content = self.editor_text.get("1.0", "end-1c").rstrip()[
                        10:
                    ]

            if current_title and current_title != "Título de la nota...":

                if self.current_note:
                    data: tuple = (
                        self.current_note,
                        current_title,
                        current_date,
                        current_content,
                    )
                    self.mediator.call_event("modify_note", data)
                else:
                    data = (current_title, current_date, current_content)
                    self.mediator.call_event("add_note", data)
        except Exception as e:
            print(f"Error en guardado final: {e}")

    def exit(self, no_save=False):
        """Salir del editor y guardar cambios finales"""

        if not no_save:
            self.save()

        # Limpiar la interfaz
        self.current_note = None
        self.pack_forget()
        self.editor_entry.delete(0, tk.END)
        self.editor_text.delete("1.0", tk.END)
