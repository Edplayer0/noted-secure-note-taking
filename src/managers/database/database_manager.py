import sqlite3

from mediator.app_mediator import AppMediator

app_mediator = AppMediator()


class DatabaseManager:

    def __init__(self, app):

        self.app = app

        app_mediator.add_service(self)

        app_mediator.add_handler("load_notes", self.load_notes)
        app_mediator.add_handler("add_note", self.add_note)
        app_mediator.add_handler("modify_note", self.modify_note)
        app_mediator.add_handler("delete_note", self.delete_note)

    def load_notes(self):

        with sqlite3.connect(self.app) as conn:

            cursor = conn.cursor()

            response = cursor.execute("SELECT * FROM Notes ORDER BY NoteId DESC;")

            notes = response.fetchall()

        notes_list = []

        for note in notes:
            note_id = note[0]
            title = app_mediator.call_event("decode", note[1])
            content = app_mediator.call_event("decode", note[2])

            notes_list.append((note_id, title, content))

        return notes_list

    def add_note(self, data: tuple[str]):

        title = app_mediator.call_event("encode", data[0])
        content = app_mediator.call_event("encode", data[1])

        with sqlite3.connect(self.app) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO notes ('NoteTitle', 'NoteContent') VALUES (?, ?)",
                (title, content),
            )

    def modify_note(self, data: tuple[int | str]):

        note_id = data[0]
        title = app_mediator.call_event("encode", data[1])
        content = app_mediator.call_event("encode", data[2])

        with sqlite3.connect(self.app) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "UPDATE notes SET NoteTitle=?, NoteContent=? WHERE NoteId = ?;",
                (
                    title,
                    content,
                    note_id,
                ),
            )

    def delete_note(self, note_id: int):

        with sqlite3.connect(self.app) as conn:

            cursor = conn.cursor()

            cursor.execute("DELETE FROM Notes WHERE NoteId = ?;", (note_id,))
