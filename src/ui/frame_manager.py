from math import ceil
from ui.notes_frame import NotesFrame
from mediator.database_mediator import DatabaseMediator

database_mediator = DatabaseMediator()


class FrameManager:

    def __init__(self, app, dashboard_frame):

        self.app = app

        self.current_frame = False

        self.notes_frames = []

        self.dashboard_frame = dashboard_frame

    def load_frames(self):

        for note_frame in self.notes_frames:
            note_frame.destroy()

        self.notes_frames.clear()

        notes = database_mediator.call_event("load_notes")

        notes_count = 0

        for _ in range(ceil(len(notes) / 4)):

            frame = NotesFrame(
                self.dashboard_frame, self.app, notes[notes_count : notes_count + 4]
            )

            self.notes_frames.append(frame)

            notes_count += 4

    def show_frames(self):

        if self.notes_frames:

            if not self.current_frame:

                self.current_frame = 0

            self.notes_frames[self.current_frame].show()

    def next_frame(self):

        try:
            self.notes_frames[self.current_frame + 1].show()
        except IndexError:
            pass
        else:
            self.notes_frames[self.current_frame].hide()
            self.current_frame += 1

    def prev_frame(self):

        if self.current_frame != 0:
            try:
                self.notes_frames[self.current_frame - 1].show()
            except IndexError:
                pass
            else:
                self.notes_frames[self.current_frame].hide()
                self.current_frame -= 1
