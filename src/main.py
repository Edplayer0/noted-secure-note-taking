# NotEd: El mejor programa de notas :)

import gc
import sys
import json
import base64
import tkinter
from tkinter import ttk
from tkinter import messagebox
from os.path import dirname, abspath
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from log_function import log

# ARCHIVOS DE LA APLICACION

PATH = dirname(abspath(__file__))

# Identificar el estado de la ejecucion
if getattr(sys, "frozen", False):
    # Si esta en uso
    PATH = dirname(sys.executable)
    try:
        PASSWORD_FILE = f"{PATH}\\password.json"
        NOTES_FILE = f"{PATH}\\notas.json"
        BACKUP_FILE = f"{PATH}\\Backup\\backup.json"
        LOG_FILE = f"{PATH}\\log.txt"
        ICON = f"{sys._MEIPASS}\\icon.ico"
        log(LOG_FILE, "APLICACION EN ESTADO DE USO")
    except Exception as e:
        messagebox.showerror("Error", e)
else:
    # Si esta en desarrollo
    try:
        PASSWORD_FILE = f"{PATH}\\password.json"
        NOTES_FILE = f"{PATH}\\notas.json"
        BACKUP_FILE = f"{PATH}\\Backup\\backup.json"
        LOG_FILE = f"{PATH}\\log.txt"
        ICON = f"{PATH}\\icon.ico"
        log(LOG_FILE, "APLICACION EN ESTADO DE DESARROLLO")
    except Exception as e:
        messagebox.showerror("Error", e)


# Variables globales

af: int = 0
titulo_dict = None
notas_frames: dict = {}


# VERIFICACION DE CONTRASENA


def verificar_contrasena(password: bytearray) -> None:
    global datosp

    try:
        with open(PASSWORD_FILE, "r", encoding="UTF-8") as passw:
            datosp = json.load(passw)
    except Exception as e:
        log(LOG_FILE, f"ERROR AL ABRIR EL ARCHIVO: {e}")
        sys.exit()

    truepass = base64.urlsafe_b64decode(datosp[0])
    salt1 = base64.urlsafe_b64decode(datosp[1])
    salt2 = base64.urlsafe_b64decode(datosp[2])

    derivacion1 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt1,
        iterations=200000
    )
    derivacion2 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt2,
        iterations=200000
    )

    try:
        posible_pass = derivacion1.derive(bytes(password))
        notas_pass = derivacion2.derive(bytes(password))
    finally:
        for datos in enumerate(password):
            index = datos[0]
            password[index] = 0
        del password
        gc.collect()

    if constant_time.bytes_eq(posible_pass, truepass):
        del posible_pass, truepass
        global cipher
        cipher = Fernet(base64.urlsafe_b64encode(notas_pass))
        del notas_pass
        gc.collect()
        log(LOG_FILE, "SESSION INICIADA CORRECTAMENTE")
        inicio()
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")

# CAMBIAR LOS FRAMES


def next_frame() -> None:
    global af

    try:
        type(notas_frames[af+1])
        notas_frames[af].pack_forget()
        af += 1
        notas_frames[af].pack(fill="both", expand=True)
    except KeyError:
        pass


def prev_frame() -> None:
    global af

    try:
        type(notas_frames[af-1])
        notas_frames[af].pack_forget()
        af -= 1
        notas_frames[af].pack(fill="both", expand=True)
    except KeyError:
        pass


# GUARDAR


def guardar(opciones: int) -> None:

    global notasjson

    match opciones:
        case 1:
            notasjson[titulo_dict] = base64.urlsafe_b64encode(
                cipher.encrypt(editor_text.get("1.0", "end-1c").rstrip().encode())).decode('utf-8')

            with open(NOTES_FILE, "w", encoding="UTF-8") as notas:
                json.dump(notasjson, notas, indent=4)

        case 2:

            notasjson[base64.urlsafe_b64encode(cipher.encrypt(editor_entry.get().strip().encode())).decode('utf-8')] = base64.urlsafe_b64encode(
                cipher.encrypt(editor_text.get("1.0", "end-1c").rstrip().encode())).decode('utf-8')

            with open(NOTES_FILE, "w", encoding="UTF-8") as notas:
                json.dump(notasjson, notas, indent=4)

        case 3:
            notasjson2 = {}

            for titulo in notasjson.keys():
                if cipher.decrypt(base64.urlsafe_b64decode(titulo)).decode('utf-8') != titulo_original:
                    notasjson2[titulo] = notasjson[titulo]
                else:
                    notasjson2[base64.urlsafe_b64encode(cipher.encrypt(editor_entry.get().strip().encode())).decode(
                        'utf-8')] = base64.urlsafe_b64encode(cipher.encrypt(editor_text.get("1.0", "end-1c").rstrip().encode())).decode('utf-8')

            with open(NOTES_FILE, "w", encoding="UTF-8") as notas:
                json.dump(notasjson2, notas, indent=4)

# ATRAS


def atras() -> None:

    global notas_frames

    if editor_entry.get().strip() == "Título de la nota..." or editor_entry.get().strip() == "":
        messagebox.showerror("Error", "El titulo no puede estar vacio")
        return
    opciones: int = 0
    if titulo_original == editor_entry.get():
        # TITULO IGUAL
        opciones = 1
    elif titulo_original == "":
        # NUEVA NOTA
        opciones = 2
    else:
        # CAMBIO DE TITULO
        opciones = 3
    guardar(opciones)
    editor_entry.delete(0, tkinter.END)
    editor_text.delete("1.0", "end")

    regresar.pack_forget()
    borrar_boton.pack_forget()
    editor.pack_forget()
    footer.pack(fill="x", side="bottom")
    titulo_header.pack(side="left")
    boton_menu.pack(side="right")

    for item in notas_frames.items():
        item[1].destroy()

    del notas_frames
    notas_frames = {}
    inicio()


# BORRAR NOTA

def borrar_nota():
    if titulo_original != "":

        confirmacion = messagebox.askyesno(
            title="Confirmación",
            message=f"Realmente desea eliminar \"{titulo_original}\"?"
        )
        if confirmacion:
            global notasjson
            del notasjson[titulo_dict]
            with open(NOTES_FILE, "w", encoding="UTF-8") as notas:
                json.dump(notasjson, notas, indent=4)
            log(LOG_FILE, "NOTA ELIMINADA")
        else:
            return

    regresar.pack_forget()
    borrar_boton.pack_forget()
    editor.pack_forget()
    titulo_header.pack(side="left")
    boton_menu.pack(side="right")
    footer.pack(fill="x", side="bottom")
    editor_entry.delete(0, tkinter.END)
    editor_text.delete("1.0", "end")
    global notas_frames

    for frame in notas_frames.items():
        frame[1].destroy()

    del notas_frames
    notas_frames = {}

    inicio()

# OCULTAR MENU


def menu_hide():

    menu.pack_forget()
    try:
        notas_frames[af].pack(fill="both", expand=True)
    except KeyError:
        pass
    footer.pack(fill="x", side="bottom")
    boton_menu.configure(command=menu_show)

# MOSTRAR MENU


def menu_show():
    try:
        notas_frames[af].pack_forget()
    except KeyError:
        pass
    footer.pack_forget()
    menu.pack(fill="both", expand=True)
    boton_menu.configure(command=menu_hide)


# FUNCIONES MENU

def backup():
    global datosp
    try:
        backup_file = open(BACKUP_FILE, "w", encoding="UTF-8")
        json.dump([notasjson, datosp], backup_file, indent=4)
        backup_file.close()
        log(LOG_FILE, "RESPALDO CREADO CORRECTAMENTE")
    except Exception as e:
        log(LOG_FILE, f"ERROR AL RESPALDAR: {e}")


# VENTANA
ventana = tkinter.Tk()
ventana.title("NotEd: Notas de alta seguridad")
ventana.geometry("400x500")
ventana.iconbitmap(ICON)

# INICIO DE SESION

login = tkinter.Frame(ventana, border=1, relief="solid")

saludo = tkinter.Label(login, text="\nBienvenido",
                       font=("Monotype Corsiva", "25"))
saludo.pack()

instruccion = tkinter.Label(
    login, text="\n\nIntroduce su contraseña:\n\n", font="Helvetica 15")
instruccion.pack()

entrada_contrasena = ttk.Entry(login, show="•")
entrada_contrasena.pack()

boton_login = ttk.Button(login, text="Enviar", command=lambda: verificar_contrasena(
    bytearray(entrada_contrasena.get().encode())))
boton_login.pack(pady=30)

copylabel = tkinter.Label(
    login, text="EdgarProblem ©2025. Todos los derechos reservados.", font=("Arial", "8"), fg="gray")
copylabel.pack(side="bottom")


# HEADER

header = tkinter.Frame(ventana, bg="#FFEE8C")
titulo_header = tkinter.Label(header, text="NotEd", bg="#FFEE8C",
                              font="Arial 23", pady=5, padx=10, fg="white")
boton_menu = tkinter.Button(header, text="☰", bd=0, relief="flat",
                            bg="#FFEE8C", fg="white", pady=5, padx=10, font="Arial 23", cursor="hand2", command=menu_show)
regresar = tkinter.Button(header, text="<", bd=0, relief="flat", bg="#FFEE8C",
                          fg="white", pady=5, padx=10, font="Arial 23", cursor="hand2", command=atras)
borrar_boton = tkinter.Button(header, text="X", bd=0, relief="flat",
                              bg="#FFEE8C", fg="white", pady=5, padx=10, font="Arial 23", cursor="hand2", command=borrar_nota)
header.pack(fill="x", side="top")
Noted = tkinter.Label(header, fg="white", bg="#FFEE8C",
                      font=("Segoe Script", "35"), text="NotEd")
Noted.pack()
login.pack(fill="both", expand=True, pady=30, padx=35)
entrada_contrasena.focus_set()

# FOOTER

footer = tkinter.Frame(ventana, bg="#FFEE8C")

footer.columnconfigure(0, weight=1, uniform="group1")
footer.columnconfigure(1, weight=1, uniform="group1")
footer.columnconfigure(2, weight=1, uniform="group1")
footer.columnconfigure(3, weight=1, uniform="group1")
footer.columnconfigure(4, weight=1, uniform="group1")

footer.rowconfigure(0, weight=1, uniform="group1")

flecha_izquierda = tkinter.Button(footer, text="<", bd=0, relief="flat",
                                  bg="#FFEE8C", fg="white", font="Arial 27", cursor="hand2", command=prev_frame)
flecha_izquierda.grid(column=0, row=0, sticky="nsew")
flecha_derecha = tkinter.Button(footer, text=">", bd=0, relief="flat",
                                bg="#FFEE8C", fg="white", font="Arial 27", cursor="hand2", command=next_frame)
flecha_derecha.grid(column=4, row=0, sticky="nsew")
nueva_nota = tkinter.Button(footer, text="+", bd=0, relief="flat",
                            bg="#FFEE8C", fg="white", font="Arial 27", cursor="hand2", command=lambda: show_editor(label_titulo=""))
nueva_nota.grid(column=2, row=0, sticky="nsew")

# EDITOR

editor = tkinter.Frame(ventana, bg="white")
editor_entry = tkinter.Entry(editor, font=(
    "Segoe Script", 20), relief="flat", bg="white", highlightbackground="white", highlightthickness=0)
editor_entry.pack(fill="x", padx=10, pady=10)

editor_text_frame = tkinter.Frame(editor)
editor_text_frame.columnconfigure(0, weight=1)
editor_text_frame.rowconfigure(0, weight=1)
editor_text_frame.pack(fill="both", expand=True)

editor_text = tkinter.Text(editor_text_frame, pady=20, padx=20,
                           font=("Arial", 15), border=0, wrap="word")
editor_text.grid(column=0, row=0, sticky="nsew")
scroll = tkinter.Scrollbar(editor_text_frame, command=editor_text.yview)
scroll.grid(column=1, row=0, sticky="ns")
editor_text.configure(yscrollcommand=scroll.set)

# MENU

menu = tkinter.Label(ventana, bg="white")
menu.columnconfigure(0, weight=1)
menu.rowconfigure(0, weight=1, uniform="group1")
menu.rowconfigure(1, weight=1, uniform="group1")
menu.rowconfigure(2, weight=1, uniform="group1")
menu.rowconfigure(3, weight=1, uniform="group1")
menu.rowconfigure(4, weight=1, uniform="group1")
menu.rowconfigure(5, weight=1, uniform="group1")
menu.rowconfigure(6, weight=1, uniform="group1")
menu.rowconfigure(7, weight=1, uniform="group1")

menu_copia = tkinter.Label(
    menu, text="Realizar copia de seguridad", border=1, bg="white", relief="solid", font=("Arial", "15"), cursor="hand2")
menu_cambio = tkinter.Label(
    menu, text="Cambiar contraseña", border=1, bg="white", relief="solid", font=("Arial", "15"), cursor="hand2")

menu_copia.bind("<Button-1>", lambda event: backup())

menu_copia.grid(column=0, row=0, sticky="nsew", padx=1, pady=1)
menu_cambio.grid(column=0, row=1, sticky="nsew", padx=1, pady=1)

# MOSTRAR EDITOR


def on_entry_focus_in(event):
    if editor_entry.get() == "Título de la nota...":
        editor_entry.delete(0, tkinter.END)
        editor_entry.config(fg='black')


def show_editor(titulo_dict_local=False, label_titulo=False):
    global titulo_original, titulo_dict

    titulo_original = label_titulo
    titulo_dict = titulo_dict_local

    # ESTO ES POR SI NO HAY NOTAS
    try:
        notas_frames[af].pack_forget()
    except KeyError:
        pass

    footer.pack_forget()
    titulo_header.pack_forget()
    boton_menu.pack_forget()
    regresar.pack(side="left")
    borrar_boton.pack(side="right")
    editor.pack(fill="both", expand=True)
    ventana.focus_set()

    if not label_titulo:
        editor_entry.config(fg='grey')
        editor_entry.insert(0, "Título de la nota...")
        editor_entry.bind("<FocusIn>", on_entry_focus_in)
    else:
        editor_entry.delete(0, tkinter.END)
        editor_entry.config(fg='black')
        editor_entry.insert(0, titulo_original)
        editor_text.insert(
            "1.0", cipher.decrypt(base64.urlsafe_b64decode(
                notasjson[titulo_dict])).decode('utf-8'))

    ventana.update_idletasks()

# INICIO


def inicio():

    global header, titulo, boton_menu, notas_frames, editor, notasjson

    if login:
        Noted.destroy()
        login.destroy()

    menu.pack_forget()


# HEADER

    header.pack(fill="x")
    titulo_header.pack(side="left")
    boton_menu.pack(side="right")


# NOTAS

    with open(NOTES_FILE, "r", encoding="UTF-8") as notas:
        notasjson = json.load(notas)

    note_count = 0
    f = 0
    f_i = int(str(f)[0])

    # CARGAR NOTAS

    try:
        for titulo_dict in notasjson.keys():
            try:
                type(notas_frames[f_i])
            except KeyError:
                notas_frames[f_i] = tkinter.Frame(ventana, bg="white")
                notas_frames[f_i].columnconfigure(
                    0, weight=1, uniform="group1")
                notas_frames[f_i].columnconfigure(
                    1, weight=1, uniform="group1")
                notas_frames[f_i].rowconfigure(0, weight=1, uniform="group2")
                notas_frames[f_i].rowconfigure(1, weight=1, uniform="group2")
                c = 0
                r = 0

            notas_labels = tkinter.Label(notas_frames[f_i], text=cipher.decrypt(base64.urlsafe_b64decode(titulo_dict)).decode('utf-8'), font=(
                "Segoe Script", "15"), relief="solid", borderwidth=1, bg="white")
            notas_labels.bind(
                "<Button-1>", lambda event, x=titulo_dict: show_editor(titulo_dict_local=x, label_titulo=notas_labels.cget('text')))
            notas_labels.grid(column=c, row=r, sticky="nsew", padx=1, pady=1)
            if c == 0:
                c += 1
            else:
                c = 0
                r += 1
            f += 0.25
            f_i = int(f)
            note_count += 1
        log(LOG_FILE, f"{note_count} NOTAS CARGADAS CORRECTAMENTE")
    except Exception as e:
        log(LOG_FILE, f"ERROR AL CARGAR NOTAS: {e}")

    # MOSTRAR NOTAS

    global af
    try:
        notas_frames[af].pack(fill="both", expand=True)
    except KeyError:
        try:
            notas_frames[af-1].pack(fill="both", expand=True)
            af -= 1
        except KeyError:
            log(LOG_FILE, "NADA QUE MOSTRAR")


# MOSTRAR FOOTER

    footer.pack(fill="x", side="bottom")


# MAINLOOP
ventana.mainloop()
