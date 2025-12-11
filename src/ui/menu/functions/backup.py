"""Functions to backup and restore notes database."""

import shutil
from tkinter import messagebox


def backup_notes(app_mediator):
    """Create a backup of the notes database."""
    database = app_mediator.call_event("files")["DATABASE"]
    backup_path = app_mediator.call_event("files")["BACKUP_DATABASE"]

    shutil.copy(database, backup_path)


def restore_notes(app_mediator):
    """Restore the notes database from a backup."""

    confirm = messagebox.askyesno(
        title="Restore Backup",
        message="Are you sure you want to restore the backup? This will overwrite your current notes.",
    )

    if not confirm:
        return

    database = app_mediator.call_event("files")["DATABASE"]
    backup_path = app_mediator.call_event("files")["BACKUP_DATABASE"]

    shutil.copy(backup_path, database)


REGISTRY = {
    "backup_notes": (" COPIA DE SEGURIDAD", backup_notes),
    "restore_notes": (" RESTAURAR COPIA", restore_notes),
}
