"""Unit tests for the DatabaseManager class."""

import os
import gc
import tempfile
import pytest


@pytest.fixture
def temp_db():
    """Fixture to create a temporal database."""
    # Create the temporal file
    fd, temp_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    yield temp_path  # Give the path to the test

    # Clean after the test
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except PermissionError:

        for _ in range(5):
            gc.collect()

        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except PermissionError:
                os.rename(temp_path, temp_path + ".deleted")
                os.remove(temp_path + ".deleted")


def test_database_manager(mocker, temp_db):
    """Test the DatabaseManager class methods."""

    # Mock the cipher in the data models
    cipher = mocker.Mock()
    cipher.encode.return_value = "Encoded string"
    cipher.decode.return_value = "Decoded string"

    mocker.patch("src.models.note_models.cipher", cipher)

    # pylint: disable=import-outside-toplevel
    from src.managers.database.database_manager import DatabaseManager
    from src.models.note_models import (
        NoteData,
        NewNoteData,
        ModifyNoteData,
    )
    from src.mediator.mediator import (
        Mediator,
    )
    import sqlite3

    # Mock the Mediator
    mock_mediator = mocker.Mock(spec=Mediator)
    mock_mediator.call_event.return_value = {"DATABASE": temp_db}

    # Initialize the DatabaseManager with the mocked Mediator
    db_manager = DatabaseManager(mock_mediator)

    # Create an in-memory database and set up the Notes table
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE Notes (NoteId INTEGER PRIMARY KEY, NoteTitle TEXT, NoteDate TEXT, NoteContent TEXT);"
        )
        cursor.execute(
            "INSERT INTO Notes (NoteTitle, NoteDate, NoteContent) VALUES (?, ?, ?);",
            ("Test Note", "25/09/2007", "This is a test note content."),
        )
        conn.commit()

    db_manager.database = temp_db

    try:

        # Test load_notes method
        notes = db_manager.load_notes()
        assert len(notes) == 1
        assert notes[0] == NoteData(id=1, title="Decoded string", date="25/09/2007")

        # Test load_note_content method
        content = db_manager.load_note_content(1)
        assert content == "Decoded string"

        # Test add_note method
        db_manager.add_note(
            NewNoteData(
                title="New Note", date="25/09/2007", content="New note content."
            )
        )
        notes = db_manager.load_notes()
        assert len(notes) == 2

        # Test modify_note method
        db_manager.modify_note(
            ModifyNoteData(
                id=1,
                title="Modified Note",
                date="25/09/2007",
                content="Modified content.",
            )
        )
        content = db_manager.load_note_content(1)
        assert content == "Decoded string"

        # Test delete_note method
        db_manager.delete_note(1)
        notes = db_manager.load_notes()
        assert len(notes) == 1
        assert notes[0].id == 2

        # Test encripted contents on the db
        with sqlite3.connect(temp_db) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Notes LIMIT 1;")
            note = cursor.fetchone()

            # Note title on the db
            assert note[1] == "Encoded string"

            # Note content on the db
            assert note[3] == "Encoded string"
    finally:

        del db_manager
