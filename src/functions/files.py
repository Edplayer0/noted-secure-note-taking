import sys
from os.path import dirname, abspath
from tkinter import messagebox


def app_files():

    # ARCHIVOS DE LA APLICACION
    file_path = f"{dirname(abspath(__file__))}\\.."

    files = {}

    # Identificar el estado de la ejecucion
    if getattr(sys, "frozen", False):
        # Si esta en uso
        file_path = dirname(sys.executable)
        try:
            files["PASSWORD_FILE"] = f"{file_path}\\password.json"
            files["NOTES_FILE"] = f"{file_path}\\notas.db"
            files["BACKUP_FILE"] = f"{file_path}\\Backup\\backup.json"
            files["LOG_FILE"] = f"{file_path}\\log.txt"
            files["ICON"] = f"{sys._MEIPASS}\\bitmap.ico"
            # log(LOG_FILE, "APLICACION EN ESTADO DE USO")
        except Exception as e:
            messagebox.showerror("Error", e)
    else:
        # Si esta en desarrollo
        try:
            files["PASSWORD_FILE"] = f"{file_path}\\password.json"
            files["NOTES_FILE"] = f"{file_path}\\notas.db"
            files["BACKUP_FILE"] = f"{file_path}\\Backup\\backup.json"
            files["LOG_FILE"] = f"{file_path}\\log.txt"
            files["ICON"] = "E:\\Proyectos\\NotEd\\assets\\bitmap.ico"
            # log(LOG_FILE, "APLICACION EN ESTADO DE DESARROLLO")
        except Exception as e:
            messagebox.showerror("Error", e)

    return files
