"""NotEd"""
import gc
import base64
import getpass
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import constant_time

print("Bienvenido a NotEd, el almacenamiento definitivo de notas importantes")

password = bytearray(getpass.getpass("Ingresa la contraseña >>> ").encode())

with open("E:/Python/NotEd/password.json", "r") as passw:
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
    cipher = Fernet(base64.urlsafe_b64encode(notas_pass))
    del notas_pass
    print("\nExito! Que operacion desea realizar?")
    operacion = int(
        input("1 - Agregar nueva nota\n2 - Leer una nota\n3 - Eliminar una nota\n4 - Salir\n\n"))
    match operacion:
        case 1:

            titulo = input("Introduce un titulo: ")
            contenido = input("NOTA >>> \n")
            with open("E:/Python/NotEd/notas.json", "r") as notas:

                try:
                    notasjson = json.load(notas)
                except json.decoder.JSONDecodeError:
                    with open("E:/Python/NotEd/notas.json", "w") as notas:
                        json.dump({}, notas, indent=4)
                        notasjson = {}

                notasjson[titulo] = base64.urlsafe_b64encode(
                    cipher.encrypt(contenido.encode())).decode('utf-8')
                with open("E:/Python/NotEd/notas.json", "w") as notas:
                    json.dump(notasjson, notas, indent=4)

        case 2:

            with open("E:/Python/NotEd/notas.json", "r") as notas:
                notasjson = json.load(notas)

            print("\nSelecciona una nota de a continuacion:\n")
            i = 0

            for titulo in notasjson.keys():
                i += 1
                print(str(i) + " - " + titulo)

            print("\n")
            seleccion = int(input(">>> "))
            if seleccion > i or seleccion < 0:
                print("Esa nota no existe!")
            j = 0

            for titulo in notasjson.keys():
                j += 1

                if seleccion == j:
                    print(titulo + "\n")
                    print(cipher.decrypt(base64.urlsafe_b64decode(
                        notasjson[titulo])).decode())
                    break

        case 3:

            with open("E:/Python/NotEd/notas.json", "r") as notas:
                notasjson = json.load(notas)

            print("Selecciona la nota a eliminar:")

            i = 0
            for titulo in notasjson.keys():
                i += 1
                print(str(i) + " - " + titulo)

            seleccion = int(input("\n>>> "))
            j = 0

            for titulo in notasjson.keys():
                j += 1

                if seleccion == j:
                    decision = input(
                        "Estas seguro de querer eliminar \'" + titulo + "\'? (S/N) ")
                    if decision == "S":
                        k = 0
                        newnotas = {}
                        for titulo in notasjson.keys():
                            k += 1
                            if k != seleccion:
                                newnotas[titulo] = notasjson[titulo]
                        with open("E:/Python/NotEd/notas.json", "w") as notas:
                            json.dump(newnotas, notas, indent=4)

        case 4:
            print("Saliendo...")

else:
    del truepass, posible_pass
    print("Contraseña incorrecta")
