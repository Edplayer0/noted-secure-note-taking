from tkinter import messagebox


def delete_note(app, app_mediator):

    confirmacion = messagebox.askyesno(
        "Confirmacion", "¿Realmente deseas eliminar esta nota?"
    )

    if confirmacion:

        current_note = app_mediator.call_event("current_note")

        if current_note:
            app_mediator.call_event("delete_note", current_note)
            app_mediator.call_event("close_editor", True)

        else:
            app_mediator.call_event("close_editor", True)
