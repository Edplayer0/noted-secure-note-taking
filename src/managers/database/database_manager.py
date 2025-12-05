import sqlite3

from mediator.mediator import Mediator


class DatabaseManager:

    def __init__(self, app_mediator: Mediator):

        self.database = app_mediator.call_event("files")["DATABASE"]

        self.mediator = app_mediator

        self.mediator.add_handler("load_notes", self.load_notes)
        self.mediator.add_handler("load_note_content", self.load_note_content)
        self.mediator.add_handler("add_note", self.add_note)
        self.mediator.add_handler("modify_note", self.modify_note)
        self.mediator.add_handler("delete_note", self.delete_note)

    def load_notes(self) -> list[tuple[int, str]]:
        """Load the list of notes from the database"""

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            response = cursor.execute(
                "SELECT NoteId, NoteTitle, NoteDate FROM Notes ORDER BY NoteId DESC;"
            )

            notes = response.fetchall()

        notes_list = []

        for note in notes:
            note_id = note[0]
            title = self.mediator.call_event("decode", note[1])
            date = note[2]

            notes_list.append((note_id, title, date))

        return notes_list

    def load_note_content(self, note_id: int) -> str:
        """Load the content of a note from the database"""

        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT NoteContent from Notes WHERE NoteID = ?;", (note_id,)
            )

            encoded_content = cursor.fetchone()[0]
            decoded_content = self.mediator.call_event("decode", encoded_content)

            return decoded_content

    def add_note(self, data: tuple[str]):

        title = self.mediator.call_event("encode", data[0])
        date = data[1]
        content = self.mediator.call_event("encode", data[2])

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO notes ('NoteTitle', 'NoteDate', 'NoteContent') VALUES (?, ?, ?)",
                (title, date, content),
            )

    def modify_note(self, data: tuple[int | str]):

        note_id = data[0]
        title = self.mediator.call_event("encode", data[1])
        date = data[2]
        content = self.mediator.call_event("encode", data[3])

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

    def delete_note(self, note_id: int):

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute("DELETE FROM Notes WHERE NoteId = ?;", (note_id,))
