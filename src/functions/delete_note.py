from tkinter import messagebox


def delete_note(app):

    confirmacion = messagebox.askyesno(
        "Confirmacion",
        "¿Realmente deseas eliminar esta nota?"
    )

    if confirmacion:

        current_note = app.dashboard.editor.current_note

        if current_note:
            app.database_manager.delete_note(current_note)
            app.dashboard.editor.exit(no_save=True)

        else:
            app.dashboard.editor.exit(no_save=True)
