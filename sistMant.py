import os
import time
import sqlite3
from prettytable import PrettyTable

def Welcome(t):

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
    print("\t<6> Ordenar asc")
    print("\t<7> Salir")
    print("----------------------------------------")
    print("\n")

    while True:

        leer = int(input("Ingrese opcion = "))

        if leer > 0 and leer < 8 :
            os.system("clear")
            break;


    NumberOpt(leer)

def IngresarAlumno():
    
    print("Ingrese los datos del Alumno\n")

    cod = input("Código : ")
    ape = input("Apellidos : ")
    nom = input("Nombres : ")
    eda = int(input("Edad : "))

    c.execute("INSERT INTO Alumnos VALUES ('{}','{}','{}','{}')"
            .format(cod,ape,nom,eda))
    

    print("\n")

    conn.commit()
    Menu()

def Reporte():
    print("Reporte de la base de datos Alumnos\n")

    x = PrettyTable()
    x.field_names = ["Código", "Apellidos", "Nombres", "Edad"]

    for rows in  c.execute("SELECT * FROM Alumnos"):
        x.add_row(rows)

    print(x)
    Menu()

def Buscar():
    print("Ingrese el código del Alumno para proceder a BUSCAR\n")

    x = PrettyTable()
    x.field_names = ['Cód-AL', 'Apellidos', 'Nombres', 'Edad', 'Cód-Curso', 'pc1', 'pc2', 'pc3']

    cod = input("Código : ")

    c.execute("SELECT * FROM Alumnos NATURAL JOIN Alumnos_Notas WHERE codigo_AI='{}'".format(cod))

    x.add_row(c.fetchall()[0])

    print(x)
    Menu()

def Eliminar():
    print("Ingrese el código del Alumno para proceder a ELIMINAR\n")

    cod = input("Código : ")
    c.execute("DELETE FROM Alumnos WHERE codigo_AI='{}'"
            .format(cod))

    conn.commit()

    c.execute("DELETE FROM Alumnos_Notas WHERE Codigo_c='{}'"
            .format(cod))

    conn.commit()
    Menu()

def Modificar():
    print("Escriba donde se desea modificar, de lo contrario dejelo vacio\n")

    cod = input("Código : ")
    c.execute("SELECT * FROM Alumnos NATURAL JOIN Alumnos_Notas WHERE codigo_AI='{}'".format(cod))

    alumno = c.fetchone()

    codiAL = alumno[0]
    ape = str(input("Apellidos ({}) : ".format(alumno[1])))
    nom = str(input("Nombre ({}) : ".format(alumno[2])))
    edad = str(input("Edad ({}) : ".format(alumno[3])))
    codiCu = alumno[4]
    pc1 = str(input("PC1 ({}) : ".format(alumno[5])))
    pc2 = str(input("PC2 ({}) : ".format(alumno[6])))
    pc3 = str(input("PC3 ({}) : ".format(alumno[7])))

    modify = [codiAL,ape,nom,edad,codiCu,pc1,pc2,pc3]

    for num,param in enumerate(modify):
        if param == "":
            modify[num] = alumno[num]

    c.execute("UPDATE Alumnos SET Apellidos='{0}', Nombres='{1}', Edad='{2}' WHERE codigo_AI='{3}'".format(modify[1],modify[2],modify[3],cod))
    conn.commit()

    c.execute("UPDATE Alumnos_Notas SET pc1='{0}', pc2='{1}', pc3='{2}' WHERE codigo_AI='{3}'".format(modify[5],modify[6],modify[7],cod))
    conn.commit()

    Menu()

def Ordenar():
    
    cod = input("Código : ")

    x = PrettyTable()
    x.field_names = ['Cód-AL', 'Apellidos', 'Nombres', 'Edad', 'Cód-Curso', 'pc1', 'pc2', 'pc3']

    for rows in c.execute("SELECT * FROM Alumnos NATURAL JOIN Alumnos_Notas ORDER BY codigo_AI ASC, Apellidos ASC"):
        x.add_row(rows)

    print(x)

    Menu()


def Salir():

    conn.close()
    return 0

def NumberOpt(arg):

    switcher = {
            1 : IngresarAlumno,
            2 : Reporte,
            3 : Buscar,
            4 : Eliminar,
            5 : Modificar,
            6 : Ordenar,
            7 : Salir
            }
    func = switcher.get(arg)
    
    func()

if __name__=="__main__":

    conn = sqlite3.connect('mantenimiento.db')
    c = conn.cursor()

    Welcome(0)
    Menu()



