import sqlite3


class DatabaseManager:

    def __init__(self, app):

        self.app = app

        self.database = self.app.files["NOTES_FILE"]

    def load_notes(self):

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            response = cursor.execute(
                "SELECT * FROM Notes ORDER BY NoteId DESC;")

            notes = response.fetchall()

        return [(note[0], self.app.cipher.decode(note[1]), self.app.cipher.decode(note[2])) for note in notes]

    def add_note(self, data):

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO notes ('NoteTitle', 'NoteContent') VALUES (?, ?)",
                (self.app.cipher.encode(data[0]), self.app.cipher.encode(data[1])))

    def modify_note(self, data):

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "UPDATE notes SET NoteTitle=?, NoteContent=? WHERE NoteId = ?;",
                (self.app.cipher.encode(data[1]), self.app.cipher.encode(data[2]), data[0]))

    def delete_note(self, note_id):

        with sqlite3.connect(self.database) as conn:

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM Notes WHERE NoteId = ?;", (note_id,))
