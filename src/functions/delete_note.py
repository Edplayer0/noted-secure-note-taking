from tkinter import messagebox

from mediator.app_mediator import AppMediator

app_mediator = AppMediator()


def delete_note(app):

    confirmacion = messagebox.askyesno(
        "Confirmacion", "¿Realmente deseas eliminar esta nota?"
    )

    if confirmacion:

        current_note = app.dashboard.editor.current_note

        if current_note:
            app_mediator.call_event("delete_note", current_note)
            app_mediator.call_event("close_editor", True)

        else:
            app_mediator.call_event("close_editor", True)
