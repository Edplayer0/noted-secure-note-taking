import sys
import sqlite3

from pathlib import Path

from src.mediator.mediator import Mediator


def app_files(app_mediator: Mediator) -> None:
    """Adds a event called 'files' to the mediator
    which returns a dict with the paths"""

    # ARCHIVOS DE LA APLICACION
    files_folder = Path.cwd() / "files"

    if not files_folder.exists():
        files_folder.mkdir()

        with sqlite3.connect(files_folder / "notas.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE Notes
            (NoteId INTEGER PRIMARY KEY, NoteTitle TEXT,
            NoteDate TEXT, NoteContent TEXT);"""
            )
        conn.commit()

        with open(files_folder / "password.json", "w", encoding="utf-8") as password:
            password.write("[]")

    files = {}

    files["PASSWORD_FILE"] = files_folder / "password.json"
    files["DATABASE"] = files_folder / "notas.db"
    files["BACKUP_DATABASE"] = files_folder / "notas-backup.db"

    if hasattr(sys, "frozen"):
        files["ICON"] = Path(sys._MEIPASS) / "bitmap.ico"
    else:
        files["ICON"] = Path.cwd() / "assets" / "bitmap.ico"

    app_mediator.add_handler("files", lambda: files)
