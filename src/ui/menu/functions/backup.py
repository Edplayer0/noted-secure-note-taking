import shutil
from os.path import dirname
from tkinter import messagebox

def backup_notes(app_mediator):
    database = app_mediator.call_event("files")["DATABASE"]
    backup_path = app_mediator.call_event("files")["BACKUP_DATABASE"]

    shutil.copy(database, backup_path)


def restore_notes(app_mediator):

    confirm = messagebox.askyesno(
        title="Restore Backup",
        message="Are you sure you want to restore the backup? This will overwrite your current notes.",
    )

    if not confirm:
        return
    
    database = app_mediator.call_event("files")["DATABASE"]
    backup_path = app_mediator.call_event("files")["BACKUP_DATABASE"]

    shutil.copy(backup_path, database)