from ui.editor import Editor
from ui.header import Header
from ui.footer.footer import Footer
from ui.frame_manager import FrameManager

from tkinter import Frame
from mediator.app_mediator import AppMediator

app_mediator = AppMediator()


class Dashboard:

    def __init__(self, app):

        self.dashboard_frame = Frame(app)

        self.header = Header(app)
        self.frames_manager = FrameManager(self.dashboard_frame)
        self.editor = Editor(app)

        self.footer = Footer(app)

        app_mediator.add_handler("open_dashboard", self.show)
        app_mediator.add_handler("open_editor", self.exit)
        app_mediator.add_handler("close_editor", self.show)

    def show(self):

        self.frames_manager.load_frames()
        self.frames_manager.show_frames()

        self.dashboard_frame.pack(fill="both", expand=True)

    def exit(self):

        self.dashboard_frame.pack_forget()
