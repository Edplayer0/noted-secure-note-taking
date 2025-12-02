from math import ceil
from ui.notes_frame import NotesFrame
from mediator.app_mediator import AppMediator


app_mediator = AppMediator()


class FrameManager:

    def __init__(self, dashboard_frame):

        self.current_frame = False

        self.notes_frames = []

        self.dashboard_frame = dashboard_frame

        app_mediator.add_handler("prev_frame", self.prev_frame)
        app_mediator.add_handler("next_frame", self.next_frame)

    def load_frames(self):

        for note_frame in self.notes_frames:
            note_frame.destroy()

        self.notes_frames.clear()

        notes = app_mediator.call_event("load_notes")

        notes_count = 0

        for _ in range(ceil(len(notes) / 4)):

            frame = NotesFrame(
                self.dashboard_frame, notes[notes_count : notes_count + 4]
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
