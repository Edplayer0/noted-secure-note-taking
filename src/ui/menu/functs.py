"""Menu functions module"""

import shutil
from tkinter import messagebox

from pathlib import Path

from src.ui.menu.register import Register
from src.mediator.mediator import Mediator
from src.models.note_models import NoteData


@Register.registry(" MAKE BACKUP")
def backup_notes(app_mediator: Mediator) -> None:
    """Create a backup of the notes database."""
    database = app_mediator.call_event("files")["DATABASE"]
    backup_path = app_mediator.call_event("files")["BACKUP_DATABASE"]

    shutil.copy(database, backup_path)


@Register.registry(" RESTORE BACKUP")
def restore_notes(app_mediator: Mediator) -> None:
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

    app_mediator.call_event("load_frames")


@Register.registry(" EXPORT TO TXT")
def export_to_txt(app_mediator: Mediator) -> None:
    """Export all the notes to a txt file"""

    confirm = messagebox.askyesno(
        "Confirm",
        "Do you want to export all notes? Every note will be decrypted and accesible in a txt file.",
    )

    if not confirm:
        return

    file_content = ""

    notes: list[NoteData] = app_mediator.call_event("load_notes")[::-1]

    line = f"{"-" * 30}\n\n"

    for note in notes:

        if file_content:
            separator = line
        else:
            separator = "\n"

        title = note.title.upper()
        date = note.date
        content = app_mediator.call_event("load_note_content", note.id)

        string = f"{separator}{title}  ({date}) \n\n{content}\n\n"

        file_content += string

    file_path = Path("notes.txt")

    quantity = len(notes)

    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(file_content)

    messagebox.showinfo(
        "Export",
        f"{quantity} notes successfully exported to: '{str(file_path.absolute())}'",
    )
