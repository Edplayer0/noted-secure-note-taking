import tkinter as tk
from customtkinter import CTkScrollbar


class Editor(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.app = master
        self.config(bg="white")

        self.current_note = None

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

        # Bind para detectar cambios
        self.editor_entry.bind("<KeyRelease>", self._on_content_change)

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

        # Bind para detectar cambios en el texto
        self.editor_text.bind("<KeyRelease>", self._on_content_change)

        self.scroll = CTkScrollbar(
            self.editor_text_frame, command=self.editor_text.yview, bg_color="white"
        )
        self.scroll.grid(column=1, row=0, sticky="ns")
        self.editor_text.configure(yscrollcommand=self.scroll.set)

    def _on_content_change(self, event=None):
        """Método para manejar cambios en el contenido"""
        # Puedes usar esto para guardado automático o validación

    def enter(self, data=False):
        """Mostrar el editor y preparar para edición"""
        self.app.dashboard.exit()
        self.app.dashboard.header.alter_mode()

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
            self.current_note = None
            self.editor_entry.config(fg="grey")
            self.editor_entry.insert(0, "Título de la nota...")
            self.editor_entry.bind("<FocusIn>", on_entry_focus_in)
        else:
            # Editar nota existente
            self.current_note = data[0]
            title = data[1]
            content = data[2]

            self.editor_entry.config(fg="black")
            self.editor_entry.insert(0, title)
            self.editor_text.insert("1.0", content)

            self.update_idletasks()

    def save(self):
        """Guardar cambios"""
        try:
            current_title = self.editor_entry.get().strip()
            current_content = self.editor_text.get("1.0", "end-1c").strip()

            if (
                current_title
                and current_title != "Título de la nota..."
                and current_content
            ):

                if self.current_note:
                    data = (self.current_note, current_title, current_content)
                    self.app.database_manager.modify_note(data)
                else:
                    data = (current_title, current_content)
                    self.app.database_manager.add_note(data)
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

        self.app.dashboard.header.alter_mode()
        self.app.dashboard.show()
