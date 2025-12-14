"""Database manager module."""

import sqlite3

from src.mediator.mediator import Mediator

from src.models.note_models import (
    NoteData,
    NewNoteData,
    ModifyNoteData,
    NoteContentData,
)


class DatabaseManager:
    """Manages the database operations related to notes.

    Args:
        app_mediator (Mediator): The application mediator for event handling.

    Methods:
        load_notes() -> list[NoteData]: Load the list of notes from the database.
        load_note_content(note_id: int) -> str: Load the content of a note from the database.
        add_note(data: tuple[str, str, str]) -> None: Add a new note to the database.
        modify_note(data: tuple[int, str, str, str]) -> None: Modify an existing note in the database.
        delete_note(note_id: int) -> None: Delete a note from the database.
    """

    def __init__(self, app_mediator: Mediator):

        self.database = app_mediator.call_event("files")["DATABASE"]

        self.mediator = app_mediator

        self.mediator.add_handler("load_notes", self.load_notes)
        self.mediator.add_handler("load_note_content", self.load_note_content)
        self.mediator.add_handler("add_note", self.add_note)
        self.mediator.add_handler("modify_note", self.modify_note)
        self.mediator.add_handler("delete_note", self.delete_note)

    def load_notes(self) -> list[NoteData]:
        """Load the list of notes from the database"""

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "SELECT NoteId, NoteTitle, NoteDate FROM Notes ORDER BY NoteId DESC;"
            )

            notes = cursor.fetchall()

        notes_list = []

        for note in notes:
            note_id = note[0]
            note_title = note[1]
            note_date = note[2]

            notes_list.append(NoteData(id=note_id, title=note_title, date=note_date))

        return notes_list

    def load_note_content(self, note_id: int) -> str:
        """Load the content of a note from the database"""

        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT NoteContent from Notes WHERE NoteID = ?;", (note_id,)
            )

            note_content = NoteContentData(content=cursor.fetchone()[0])

        return note_content.content

    def add_note(self, data: NewNoteData) -> None:
        """Add a new note to the database"""

        title = data.title
        date = data.date
        content = data.content

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO notes ('NoteTitle', 'NoteDate', 'NoteContent') VALUES (?, ?, ?)",
                (title, date, content),
            )

            conn.commit()

    def modify_note(self, data: ModifyNoteData) -> None:
        """Modify an existing note in the database"""
        note_id = data.id
        title = data.title
        date = data.date
        content = data.content

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "UPDATE notes SET NoteTitle=?, NoteDate=?, NoteContent=? WHERE NoteId = ?;",
                (
                    title,
                    date,
                    content,
                    note_id,
                ),
            )

            conn.commit()

    def delete_note(self, note_id: int) -> None:
        """Delete a note from the database"""

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute("DELETE FROM Notes WHERE NoteId = ?;", (note_id,))

            conn.commit()
