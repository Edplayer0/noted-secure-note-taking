# NotEd: El mejor programa de notas :)

import gc
import base64
import json
import tkinter
from tkinter import ttk
from tkinter import messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import constant_time


af = 0
titulo_safe = 0
notas_frames = {}


# VERIFICACION DE CONTRASENA


def verificar_contrasena(password):
    global datosp
    with open("E:/Programación/Proyectos/NotEd/password.json", "r") as passw:
        datosp = json.load(passw)

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
        for i in range(len(password)):
            password[i] = 0
        del password
        gc.collect()

    if constant_time.bytes_eq(posible_pass, truepass):
        del posible_pass, truepass
        global cipher
        cipher = Fernet(base64.urlsafe_b64encode(notas_pass))
        del notas_pass
        gc.collect()
        inicio()
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")

# CAMBIAR LOS FRAMES


def next_frame():
    global af

    try:
        print(type(notas_frames[af+1]))
        notas_frames[af].pack_forget()
        af += 1
        notas_frames[af].pack(fill="both", expand=True)
    except KeyError:
        return


def prev_frame():
    global af

    try:
        print(type(notas_frames[af-1]))
        notas_frames[af].pack_forget()
        af -= 1
        notas_frames[af].pack(fill="both", expand=True)
    except KeyError:
        return


# GUARDAR


def guardar(opciones):

    global titulo_original, notasjson

    match opciones:
        case 1:
            notasjson[base64.urlsafe_b64encode(cipher.encrypt(titulo_original.encode())).decode('utf-8')] = base64.urlsafe_b64encode(
                cipher.encrypt(editor_text.get("1.0", "end-1c").rstrip().encode())).decode('utf-8')

            with open("E:/Programación/Proyectos/NotEd/notas.json", "w") as notas:
                json.dump(notasjson, notas, indent=4)

        case 2:

            notasjson[base64.urlsafe_b64encode(cipher.encrypt(editor_entry.get().strip().encode())).decode('utf-8')] = base64.urlsafe_b64encode(
                cipher.encrypt(editor_text.get("1.0", "end-1c").rstrip().encode())).decode('utf-8')

            with open("E:/Programación/Proyectos/NotEd/notas.json", "w") as notas:
                json.dump(notasjson, notas, indent=4)

        case 3:
            notasjson2 = {}

            for titulo in notasjson.keys():
                if cipher.decrypt(base64.urlsafe_b64decode(titulo)).decode('utf-8') != titulo_original:
                    notasjson2[titulo] = notasjson[titulo]
                else:
                    notasjson2[titulo_safe] = base64.urlsafe_b64encode(
                        cipher.encrypt(editor_text.get("1.0", "end-1c").rstrip().encode())).decode('utf-8')

            with open("E:/Programación/Proyectos/NotEd/notas.json", "w") as notas:
                json.dump(notasjson2, notas, indent=4)

# ATRAS


def atras():

    global notas_frames

    if editor_entry.get().strip() == "Título de la nota..." or editor_entry.get().strip() == "":
        messagebox.showerror("Error", "El titulo no puede estar vacio")
        return
    opciones = 0
    if titulo_original == editor_entry.get():
        # TITULO IGUAL
        opciones = 1
    elif titulo_original == "":
        # NUEVA NOTA
        opciones = 2
    else:
        # CAMBIO DE TITULO
        opciones = 3
    print(opciones)
    guardar(opciones)
    editor_entry.delete(0, tkinter.END)
    editor_text.delete("1.0", "end")

    regresar.pack_forget()
    borrar_boton.pack_forget()
    editor.pack_forget()
    footer.pack(fill="x", side="bottom")
    titulo.pack(side="left")
    boton_menu.pack(side="right")

    for frame in notas_frames.keys():
        notas_frames[frame].destroy()

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
            del notasjson[titulo_original]
            with open("E:/Programación/Proyectos/NotEd/notas.json", "w") as notas:
                json.dump(notasjson, notas, indent=4)
        else:
            return

    regresar.pack_forget()
    borrar_boton.pack_forget()
    editor.pack_forget()
    titulo.pack(side="left")
    boton_menu.pack(side="right")
    footer.pack(fill="x", side="bottom")
    editor_entry.delete(0, tkinter.END)
    editor_text.delete("1.0", "end")
    global notas_frames

    for frame in notas_frames.keys():
        notas_frames[frame].destroy()

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
    backup_file = open(
        "E:/Programación/Proyectos/NotEd/backup/backup.json", "w")
    json.dump([notasjson, datosp], backup_file, indent=4)
    backup_file.close()


# def ram_salts():
#    salt3 = os.urandom(16)
#    derivacion3 = PBKDF2HMAC(
#        algorithm=hashes.SHA256(),
#        length=32,
#        salt=salt3,
#        iterations=200000
#    )
#    cipher2 =
#    for titulo in notasjson.keys():
#        notasjson[titulo] = cipher.decrypt(
#            base64.urlsafe_b64decode(notasjson[titulo])).decode()


# VENTANA
ventana = tkinter.Tk()
ventana.title("NotEd: Notas de alta seguridad")
ventana.geometry("400x500")

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
titulo = tkinter.Label(header, text="NotEd", bg="#FFEE8C",
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
                            bg="#FFEE8C", fg="white", font="Arial 27", cursor="hand2", command=lambda: show_editor("", ""))
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
menu_salt = tkinter.Label(
    menu, text="Randomizar salts", border=1, bg="white", relief="solid", font=("Arial", "15"), cursor="hand2")

menu_copia.bind("<Button-1>", lambda event: backup())

menu_copia.grid(column=0, row=0, sticky="nsew", padx=1, pady=1)
menu_cambio.grid(column=0, row=1, sticky="nsew", padx=1, pady=1)
menu_salt.grid(column=0, row=2, sticky="nsew", padx=1, pady=1)

# MOSTRAR EDITOR


def on_entry_focus_in(event):
    if editor_entry.get() == "Título de la nota...":
        editor_entry.delete(0, tkinter.END)
        editor_entry.config(fg='black')


def show_editor(event, label_titulo):
    global titulo_original, titulo_safe
    if label_titulo != "":
        titulo_original = cipher.decrypt(
            base64.urlsafe_b64decode(label_titulo)).decode('utf-8')
        titulo_safe = label_titulo
    else:
        titulo_original = label_titulo

    # ESTO ES POR SI NO HAY NOTAS
    try:
        notas_frames[af].pack_forget()
    except KeyError:
        pass

    footer.pack_forget()
    titulo.pack_forget()
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
                notasjson[label_titulo])).decode('utf-8'))

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
    titulo.pack(side="left")
    boton_menu.pack(side="right")


# NOTAS

    with open("E:/Programación/Proyectos/NotEd/notas.json", "r") as notas:
        notasjson = json.load(notas)

    t = 0
    f = 0
    f_i = int(str(f)[0])

    # CARGAR NOTAS

    for titulo_dict in notasjson.keys():
        try:
            print(type(notas_frames[f_i]))
        except KeyError:
            notas_frames[f_i] = tkinter.Frame(ventana, bg="white")
            notas_frames[f_i].columnconfigure(0, weight=1, uniform="group1")
            notas_frames[f_i].columnconfigure(1, weight=1, uniform="group1")
            notas_frames[f_i].rowconfigure(0, weight=1, uniform="group2")
            notas_frames[f_i].rowconfigure(1, weight=1, uniform="group2")
            c = 0
            r = 0

        notas_labels = tkinter.Label(notas_frames[f_i], text=cipher.decrypt(base64.urlsafe_b64decode(titulo_dict)).decode('utf-8'), font=(
            "Segoe Script", "15"), relief="solid", borderwidth=1, bg="white")
        notas_labels.bind(
            "<Button-1>", lambda event, x=titulo_dict: show_editor(event, x))
        notas_labels.grid(column=c, row=r, sticky="nsew", padx=1, pady=1)
        if c == 0:
            c += 1
        else:
            c = 0
            r += 1
        f += 0.25
        f_i = int(str(f)[0])
        t += 1

    # MOSTRAR NOTAS

    global af
    try:
        notas_frames[af].pack(fill="both", expand=True)
    except KeyError:
        try:
            notas_frames[af-1].pack(fill="both", expand=True)
            af -= 1
        except KeyError:
            pass


# MOSTRAR FOOTER

    footer.pack(fill="x", side="bottom")


# FINAL
ventana.mainloop()
