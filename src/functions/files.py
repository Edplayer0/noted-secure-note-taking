"""Files manager module"""

import sys
import sqlite3

from pathlib import Path

from src.mediator.mediator import Mediator


def app_files(app_mediator: Mediator) -> None:
    """Adds a event called 'files' to the mediator
    which returns a dict with the paths to each file"""

    # Folder in which the files are stored
    files_folder = Path.cwd() / "files"

    # If the folder doesn't exist it's created
    # with the necessary files
    if not files_folder.exists():
        files_folder.mkdir()

        # create the database with sqlite3
        with sqlite3.connect(files_folder / "notes.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE Notes
            (NoteId INTEGER PRIMARY KEY, NoteTitle TEXT,
            NoteDate TEXT, NoteContent TEXT);"""
            )
        conn.commit()

        # create the password file
        with open(files_folder / "password.json", "w", encoding="utf-8") as password:
            password.write("[]")

    files = {}

    # add the paths to the dictionary
    files["PASSWORD_FILE"] = files_folder / "password.json"
    files["DATABASE"] = files_folder / "notes.db"
    files["BACKUP_DATABASE"] = files_folder / "notes-backup.db"

    # if it's an executable, use the bitmap
    # added on pyinstaller installation
    if hasattr(sys, "frozen"):
        files["ICON"] = Path(sys._MEIPASS) / "bitmap.ico"
    else:
        files["ICON"] = Path.cwd() / "assets" / "bitmap.ico"

    # add a handler which returns the dict
    app_mediator.add_handler("files", lambda: files)
