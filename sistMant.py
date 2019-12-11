import os
import time
import sqlite3
from prettytable import PrettyTable


def Welcome(t):
    # Limpiamos el shell(bash)
    os.system("clear")
    time.sleep(t)

    print("****************************************")
    print("*                                      *")
    print("*  SISTEMA DE MANTENIMIENTO 2019 - II  *")
    print("*                                      *")
    print("****************************************")

    time.sleep(t)


def Menu():

    print("\n")
    print("----------------------------------------")
    print("\t<1> Ingresar alumno")
    print("\t<2> Reporte")
    print("\t<3> Buscar")
    print("\t<4> Eliminar")
    print("\t<5> Modificar")
    print("\t<6> Ordenar")
    print("\t<7> Salir")
    print("----------------------------------------")
    print("\n")

    while True:

        leer = int(input("Ingrese opcion = "))
        # Solamente se permite el rango de 1 - 7
        if leer > 0 and leer < 8:
            os.system("clear")
            break
    NumberOpt(leer)


def Upload(t):
    print("[INFO] Cargando ...")
    time.sleep(t)

    c.execute("CREATE TABLE IF NOT EXISTS Alumnos(\
            codigo_AI varchar(9) PRIMARY KEY NOT NULL,\
            Apellidos varchar(18),\
            Nombres varchar(18),\
            Edad int\
            ); ")
    conn.commit()

    print("[INFO] Ejecutando la tabla Alumnos")
    time.sleep(t)

    c.execute("CREATE TABLE IF NOT EXISTS Cursos(\
            Codigo_c varchar(9) PRIMARY KEY NOT NULL,\
            Descripcion varchar(18),\
            Creditos int);")
    conn.commit()

    print("[INFO] Ejecutando la tabla Cursos")
    time.sleep(t)

    c.execute("CREATE TABLE IF NOT EXISTS Alumnos_Notas(\
            codigo_AI varchar(9),\
            Codigo_c varchar(9),\
            pc1 int,\
            pc2 int,\
            pc3 int,\
            FOREIGN KEY(codigo_AI) \
            REFERENCES Alumnos(codigo_AI), \
            FOREIGN KEY(Codigo_c)\
            REFERENCES Cursos(Codigo_c));")
    conn.commit()

    print("[INFO] Ejecutando la tabla Alumnos_Notas")
    time.sleep(t)

    print("[INFO] Finalizo el upload :)")
    time.sleep(t)


def IngresarAlumno():
    print("\nIngrese los datos del Alumno\n")
    # Input devuelve un tipo de variable str
    cod = str(ValidarCod("Código"))
#    cod = input("Código Alumno : ")
    ape = input("Apellidos : ")
    nom = input("Nombres : ")
    eda = int(input("Edad : "))

    cod_c = input("Código Curso : ")

    pc1 = VerificarNota("PC1")
    pc2 = VerificarNota("PC2")
    pc3 = VerificarNota("PC3")

    # insertamos desde python la sintaxis INSERT en sql
    c.execute("INSERT INTO Alumnos \
            VALUES ('{}','{}','{}','{}')".format(cod, ape, nom, eda))
    conn.commit()
    c.execute("INSERT INTO Alumnos_Notas \
        VALUES('{}','{}','{}','{}','{}')".format(cod, cod_c, pc1, pc2, pc3))
    conn.commit()

    print("\n")
    # Guarda la tarea anterior ejecutada
    Menu()


def VerificarNota(name):
    verif = -1

    while not (verif >= 0 and verif <= 20):
        verif = input("{} : ".format(name))
        if verif == "":
            return verif
        else:
            verif = int(verif)

    return verif


def ValidarCod(name):

    verif = input("{} :".format(name))

    while not (len(verif[0:8]) == 8 and (verif[8] >= 'A' and verif[8] <= 'K')):
        verif = input("{} : ".format(name))

    return verif


def Reporte():
    print("\nReporte de la base de datos Alumnos\n")

    # Es un formato de visualización de tablas
    x = PrettyTable()
    x.field_names = ["Código", "Apellidos", "Nombres", "Edad"]

    for rows in c.execute("SELECT * FROM Alumnos"):
        x.add_row(rows)

    print(x)
    Menu()


def Buscar():
    print("\nIngrese el código del Alumno para proceder a BUSCAR\n")

    x = PrettyTable()
    x.field_names = [
            'Cod-AL',
            'Apellidos',
            'Nombres',
            'Edad',
            'Cod-Curso',
            'pc1', 'pc2', 'pc3']

    cod = input("Codigo : ")

    c.execute("SELECT * FROM Alumnos\
            NATURAL JOIN Alumnos_Notas \
            WHERE codigo_AI='{}'".format(cod))
    # fetchall nos permite obtener toda las coincidencia posible
    # hacemos un mapeo a cada una de los datos para formar un tipo de lista
    # data = list(map(str, c.fetchall()[0]))
    data = c.fetchone()
    x.add_row(data)
    print(x)
    Menu()


def Eliminar():
    print("\nIngrese el código del Alumno para proceder a ELIMINAR\n")

    cod = input("Código : ")
    # Para eliminar un dato debemos ELIMINAR de las dos tablas que se usan para
    # el mismo estudiante
    c.execute("DELETE FROM Alumnos WHERE codigo_AI='{}'".format(cod))

    conn.commit()

    c.execute("DELETE FROM Alumnos_Notas WHERE Codigo_c='{}'".format(cod))

    conn.commit()
    Menu()


def Modificar():
    print("\nEscriba donde se desea modificar, de lo contrario dejelo vacio\n")

    cod = input("Código : ")
    c.execute("SELECT * FROM Alumnos NATURAL JOIN Alumnos_Notas WHERE\
            codigo_AI='{}'".format(cod))
    # Es similiar al método fetchall, la diferencia que solamente accedera al
    # dato que tenga el mismo código
    conn.commit()
    alumno = c.fetchone()

    codiAL = alumno[0]
    ape = str(input("Apellidos ({}) : ".format(alumno[1])))
    nom = str(input("Nombre ({}) : ".format(alumno[2])))
    edad = str(input("Edad ({}) : ".format(alumno[3])))
    codiCu = alumno[4]
    pc1 = str(VerificarNota("PC1 ({})".format(alumno[5])))
    pc2 = str(VerificarNota("PC2 ({})".format(alumno[6])))
    pc3 = str(VerificarNota("PC3 ({})".format(alumno[7])))

    modify = [codiAL, ape, nom, edad, codiCu, pc1, pc2, pc3]

    # Mapea nuevamente los datos modificados
    for num, param in enumerate(modify):
        if param == "":
            modify[num] = alumno[num]

    # Actualizando la base de datos

    c.execute("UPDATE Alumnos\
            SET Apellidos='{0}', Nombres='{1}', Edad='{2}'\
            WHERE codigo_AI='{3}'\
            ".format(modify[1], modify[2], int(modify[3]), modify[0]))
    conn.commit()

    c.execute("UPDATE Alumnos_Notas\
            SET pc1='{0}', pc2='{1}', pc3='{2}'\
            WHERE codigo_AI='{3}'\
            ".format(int(modify[5]), int(modify[6]), int(modify[7]), modify[0]))
    conn.commit()

    Menu()


def Ordenar():
    x = PrettyTable()
    x.field_names = [
            'Cod-AL',
            'Apellidos',
            'Nombres',
            'Edad',
            'Cod-Curso',
            'pc1',
            'pc2',
            'pc3',
            'Promedio']

    for rows in c.execute("SELECT * \
            FROM Alumnos \
            NATURAL JOIN Alumnos_Notas \
            WHERE codigo_AI \
            LIKE '_________' \
            ORDER BY codigo_AI \
            ASC"):

        prom = round((rows[-3:][0] + rows[-3:][1] + rows[-3:][2])/3, 2)
        rows = list(rows) + [prom]
        x.add_row(rows)

    print(x)

    Menu()


def Salir():

    conn.close()
    return 0


def NumberOpt(arg):

    # Lista de número con sus respectivas funciones
    switcher = {
            1: IngresarAlumno,
            2: Reporte,
            3: Buscar,
            4: Eliminar,
            5: Modificar,
            6: Ordenar,
            7: Salir
            }
    func = switcher.get(arg)
    func()


if __name__ == "__main__":
    # Cargamos la base de datos
    conn = sqlite3.connect('mantenimiento.db')
    c = conn.cursor()
    Upload(0)
    Welcome(0)
    Menu()
