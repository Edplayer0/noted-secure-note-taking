import sys
from os.path import dirname, abspath
from tkinter import messagebox

from mediator.mediator import Mediator


def app_files(app_mediator: Mediator) -> None:
    """Adds a event called 'files' to the mediator
    which returns a dict with the paths"""

    # ARCHIVOS DE LA APLICACION
    file_path = f"{dirname(abspath(__file__))}\\.."

    files = {}

    # Identificar el estado de la ejecucion
    if hasattr(sys, "frozen"):
        # Si esta en uso
        file_path = dirname(sys.executable)
        try:
            files["PASSWORD_FILE"] = f"{file_path}\\password.json"
            files["DATABASE"] = f"{file_path}\\notas.db"
            files["BACKUP_FILE"] = f"{file_path}\\Backup\\backup.json"
            files["LOG_FILE"] = f"{file_path}\\log.txt"
            files["ICON"] = f"{sys._MEIPASS}\\bitmap.ico"
        except Exception as e:
            messagebox.showerror("Error", e)
    else:
        # Si esta en desarrollo
        try:
            files["PASSWORD_FILE"] = f"{file_path}\\password.json"
            files["DATABASE"] = f"{file_path}\\notas.db"
            files["BACKUP_FILE"] = f"{file_path}\\Backup\\backup.json"
            files["LOG_FILE"] = f"{file_path}\\log.txt"
            files["ICON"] = "E:\\Proyectos\\NotEd\\assets\\bitmap.ico"
        except Exception as e:
            messagebox.showerror("Error", e)

    app_mediator.add_handler("files", lambda: files)
