"""Dashboard module for NotEd application."""

from tkinter import Frame

from ui.editor import Editor
from ui.dashboard.header import Header
from ui.dashboard.footer.footer import Footer
from ui.dashboard.notes.frame_manager import FrameManager

from mediator.mediator import Mediator

class Dashboard:
    """Dashboard class managing the main dashboard UI components."""

    def __init__(self, app, app_mediator: Mediator):

        self.mediator = app_mediator

        self.dashboard_frame = Frame(app)

        self.header = Header(app, app_mediator)
        self.frames_manager = FrameManager(self.dashboard_frame, app_mediator)
        self.editor = Editor(app, app_mediator)

        self.footer = Footer(app, app_mediator)

        self.mediator.add_handler("start", self.show)
        self.mediator.add_handler("open_editor", self.exit)
        self.mediator.add_handler("close_editor", self.show)
        self.mediator.add_handler("show_menu", self.exit)
        self.mediator.add_handler("exit_menu", self.show)

    def show(self):
        """Show the dashboard frame and load frames."""

        self.frames_manager.load_frames()
        self.frames_manager.show_frames()

        self.dashboard_frame.pack(fill="both", expand=True)

    def exit(self):
        """Hide the dashboard frame."""

        self.dashboard_frame.pack_forget()
