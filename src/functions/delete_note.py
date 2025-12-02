from tkinter import messagebox

from mediator.database_mediator import DatabaseMediator

database_mediator = DatabaseMediator()


def delete_note(app):

    confirmacion = messagebox.askyesno(
        "Confirmacion", "¿Realmente deseas eliminar esta nota?"
    )

    if confirmacion:

        current_note = app.dashboard.editor.current_note

        if current_note:
            database_mediator.call_event("delete_note", current_note)
            app.dashboard.editor.exit(no_save=True)

        else:
            app.dashboard.editor.exit(no_save=True)
