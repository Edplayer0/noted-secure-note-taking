"""Dashboard module for NotEd application."""

from tkinter import Frame

from src.ui.editor import Editor
from src.ui.dashboard.header import Header
from src.ui.dashboard.footer.footer import Footer
from src.ui.dashboard.notes.frame_manager import FrameManager

from src.mediator.mediator import Mediator


class Dashboard:
    """Dashboard class managing the main dashboard UI components."""

    def __init__(self, app, app_mediator: Mediator):

        self.mediator = app_mediator

        self.dashboard_frame = Frame(app)

        self.header = Header(app, app_mediator)
        self.frames_manager = FrameManager(self.dashboard_frame, app_mediator)
        self.editor = Editor(app, app_mediator)

        self.footer = Footer(app, app_mediator)

        self.mediator.add_handler("start", self.show, 3)
        self.mediator.add_handler("open_editor", self.exit, 1)
        self.mediator.add_handler("close_editor", self.show, 3)
        self.mediator.add_handler("show_menu", self.exit)
        self.mediator.add_handler("exit_menu", self.show)

    def show(self):
        """Show the dashboard frame and load frames."""
        self.dashboard_frame.pack(fill="both", expand=True)

    def exit(self):
        """Hide the dashboard frame."""
        self.dashboard_frame.pack_forget()
