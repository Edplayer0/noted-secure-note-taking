from ui.editor import Editor
from ui.header import Header
from ui.footer.footer import Footer
from ui.frame_manager import FrameManager

from tkinter import Frame


class Dashboard:

    def __init__(self, app):

        self.dashboard_frame = Frame(app)

        self.header = Header(app)
        self.frames_manager = FrameManager(app, self.dashboard_frame)
        self.editor = Editor(app)

        self.footer = Footer(app)

    def show(self):

        self.header.show()

        self.frames_manager.load_frames()
        self.frames_manager.show_frames()

        self.dashboard_frame.pack(fill="both", expand=True)

        self.footer.show()

    def exit(self):

        self.dashboard_frame.pack_forget()

        self.footer.hide()
