"""Manages the note frames in the dashboard."""

from math import ceil
from tkinter import Frame

from src.ui.dashboard.notes.notes_frame import NotesFrame

from src.models.note_models import NoteData

from src.mediator.mediator import Mediator


class FrameManager:
    """Manages the note frames in the dashboard."""

    def __init__(self, dashboard_frame, app_mediator: Mediator):

        self.mediator = app_mediator

        self.current_frame = False

        self.notes_frames: list[Frame] = []

        self.dashboard_frame = dashboard_frame

        self.mediator.add_handler("prev_frame", self.prev_frame)
        self.mediator.add_handler("next_frame", self.next_frame)
        self.mediator.add_handler("start", self.load_frames)
        self.mediator.add_handler("start", self.show_frames)
        self.mediator.add_handler("load_frames", self.load_frames)
        self.mediator.add_handler("load_frames", self.show_frames)

    def load_frames(self) -> None:
        """Dinamically creates the frames"""

        for note_frame in self.notes_frames:
            note_frame.destroy()

        self.notes_frames.clear()

        notes: list[NoteData] = self.mediator.call_event("load_notes")

        notes_count: int = 0

        for _ in range(ceil(len(notes) / 4)):

            frame = NotesFrame(
                self.dashboard_frame,
                notes[notes_count : notes_count + 4],
                self.mediator,
            )

            self.notes_frames.append(frame)

            notes_count += 4

    def show_frames(self) -> None:
        """Maps the current frame"""

        if self.notes_frames:

            if not self.current_frame:

                self.current_frame = 0

            try:
                self.notes_frames[self.current_frame].show()
            except IndexError:
                try:
                    self.notes_frames[self.current_frame - 1].show()
                except IndexError:
                    pass
                else:
                    self.current_frame -= 1

    def next_frame(self) -> None:
        """Show the next frame if exists"""

        try:
            self.notes_frames[self.current_frame + 1].show()
        except IndexError:
            pass
        else:
            self.notes_frames[self.current_frame].hide()
            self.current_frame += 1

    def prev_frame(self) -> None:
        """Show the previous frame if exists"""

        if self.current_frame != 0:
            try:
                self.notes_frames[self.current_frame - 1].show()
            except IndexError:
                pass
            else:
                self.notes_frames[self.current_frame].hide()
                self.current_frame -= 1
