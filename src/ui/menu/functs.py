"""Menu functions module"""

import shutil
from tkinter import messagebox

from src.ui.menu.register import Register


@Register.registry(" MAKE BACKUP")
def backup_notes(app_mediator):
    """Create a backup of the notes database."""
    database = app_mediator.call_event("files")["DATABASE"]
    backup_path = app_mediator.call_event("files")["BACKUP_DATABASE"]

    shutil.copy(database, backup_path)


@Register.registry(" RESTORE BACKUP")
def restore_notes(app_mediator):
    """Restore the notes database from a backup."""

    confirm = messagebox.askyesno(
        title="Restore Backup",
        message="Are you sure you want to restore the backup? \
This will overwrite your current notes.",
    )

    if not confirm:
        return

    database = app_mediator.call_event("files")["DATABASE"]
    backup_path = app_mediator.call_event("files")["BACKUP_DATABASE"]

    shutil.copy(backup_path, database)
