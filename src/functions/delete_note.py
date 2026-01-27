from tkinter import messagebox


def delete_note(app_mediator):

    confirmacion = messagebox.askyesno(
        "Confirm", "Do you really want to delete this note?"
    )

    if confirmacion:

        current_note = app_mediator.call_event("current_note")

        if current_note:
            app_mediator.call_event("delete_note", current_note)
            app_mediator.call_event("close_editor", True)

        else:
            app_mediator.call_event("close_editor", True)
