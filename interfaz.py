import tkinter as tk               
from tkinter import font  as tkfont 
from functools import partial
from PIL import ImageTk, Image
import sqlite3

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super(SampleApp, self).__init__()

        self.geometry("350x450")
        self.title("VALIDACIÓN DE USUARIO")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        # Creando un contenedor que nos permitirá insertar widget
        container = tk.Frame(
                self, 
                bg="#ADD8E6")

        # Le asignamos configuraciones
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # El bucle estará interactuando cuando se inicie sesión con las opciones
        for F in (Ingresar, Salir):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # sticky refencia la posición absoluta del widget con el padre
            frame.grid(row=0, column=0, sticky="nsew", padx=20)

        self.show_frame("Ingresar")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Ingresar(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.config(bg="#ADD8E6")
        self.controller = controller

        self.contra = BaseDato.Contra()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        imagen = Image.open("./UNI.png")
        imagen = imagen.resize((250,90), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imagen)
        
        label = tk.Label(
                self, 
                image = img, 
                bg="#ADD8E6")
        
        label.image = img
        label.grid(row=0, column=0, columnspan=2)

        self.small_font = ('Verdana',15)

        lbl_user = tk.Label(
                self,
                text="USUARIO: ",
                font=self.small_font, 
                bg="#ADD8E6",
                fg="black")

        lbl_user.grid(row=1, column=0, pady=20)

        self.entry_text = tk.StringVar() 
        self.entry_text_pass = tk.StringVar() 

        edit_user = tk.Entry(self, 
                width=10, 
                textvariable=self.entry_text, 
                font=self.small_font)

        edit_user.grid(row=1, column=1)

        lbl_pass = tk.Label(
                self, 
                text="CONTRASEÑA: ",
                font=self.small_font, 
                bg="#ADD8E6", 
                fg="black")

        lbl_pass.grid(row=2, column=0, pady=20)

        self.edit_user = tk.Entry(
                self,
                width=10, 
                textvariable=self.entry_text_pass,
                font=self.small_font,
                show="*")

        self.edit_user.grid(row=2, column=1)

        btn_user = tk.Button(
                self, 
                text="Ingresar",
                command=lambda : self.compare())

        btn_user.grid(row=3, column=0)

        btn_pass = tk.Button(
                self, 
                text="Salir", 
                command= self.close_it)

        btn_pass.grid(row=3, column=1)

        self.entry_text.trace("w", lambda *args: self.character_limit())
        self.entry_text_pass.trace("w", lambda *args: self.character_limit())

    def character_limit(self):
        if len(self.entry_text.get()) > 0:
            self.entry_text.set(self.entry_text.get()[:9])

    def character_limit_pass(self):
        if len(self.entry_text_pass.get()) > 0:
            self.entry_text_pass.set(self.entry_text.get()[:9])

    def compare(self):

        if any([x == self.entry_text.get() 
            for x in self.contra]) and any(x==self.entry_text_pass.get()
                    for x in self.contra):

            self.lbl_msm = tk.Label(
                    self, 
                    text="",
                    bg="#ADD8E6", 
                    width=10, 
                    font=self.small_font)

            self.lbl_msm.grid(row=4, column=0, columnspan=2, padx=50,sticky="s")
            self.controller.show_frame("Salir")

        else:

            self.lbl_msm = tk.Label(
                    self,
                    text="Incorrecto",
                    bg="#ADD8E6",
                    fg="red")

            self.lbl_msm.grid(row=4, column=0, columnspan=2, pady=10,sticky="s")


    def close_it(self):
        self.quit()
        self.destroy()

class PageOne(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.open_another()

    def close_it(self):
        self.id.destroy()

    def open_another(self):
        self.id = tk.Toplevel(self.parent)

        label = tk.Label(
                self.id, 
                text="MENU DE OPCIONES")

        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(
                self.id, 
                text="Go", 
                command=self.close_it)

        button.pack()

class Salir(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg="#ADD8E6")

        label = tk.Label(
                self, 
                text="MENU DE OPCIONES", 
                font=controller.title_font,
                bg="#ADD8E6", 
                fg="black")

        label.pack(side="top", fill="both", pady=30)

        self.v = tk.IntVar()
  
        self.Alumno = tk.Radiobutton(
                self, 
                text="Alumnos", 
                indicatoron=0, 
                variable=self.v, 
                value=1,
                justify="center", 
                width=10,
                fg="black", 
                command= lambda: self.getScript()).pack(side="top",pady=5)
        
        self.Cursos = tk.Radiobutton(
                self,
                text="Cursos", 
                indicatoron=0, 
                variable=self.v, 
                value=2, 
                justify="center", 
                width=10,
                fg="black", 
                command= lambda: self.getScript()).pack(side="top",pady=5)

        self.Notas = tk.Radiobutton(
                self, 
                text="Notas", 
                indicatoron=0, 
                variable=self.v, 
                value=3,
                justify="center", 
                width=10,
                fg="black",
                command=lambda : self.getScript()).pack(side="top",pady=5)


        button = tk.Button(
                self, 
                text="Cerrar Sesion",
                bg="orange",
                command=lambda: controller.show_frame("Ingresar"))
        button.pack()

    def getScript(self):

        if self.v.get() == 1:
            Alumnos(self)

        elif self.v.get() == 2:
            Cursos(self)

        elif self.v.get() == 3:
            Notas(self)


class Alumnos(tk.Frame):

    global BaseDato

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)


        self.parent = parent
        self.open_another()

    def close_it(self):
        self.id.destroy()

    def open_another(self):
        self.id = tk.Toplevel(self.parent)

        alumn = BaseDato.Reporte()

        for r in range(0,len(alumn)):
            for c in range(0, len(alumn[0])):
                var = tk.StringVar()

                var.set(alumn[r][c])

                cell = tk.Label(
                        self.id, 
                        width=15, 
                        justify="center", 
                        bg="#ADD8E6", 
                        fg="black",
                        textvariable=var,
                        borderwidth=2, 
                        relief="groove")

                cell.grid(row=r, column=c)

class Cursos(tk.Frame):

    global BaseDato

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.open_another()

    def close_it(self):
        self.id.destroy()

    def open_another(self):
        self.id = tk.Toplevel(self.parent)
        
        alumn_not = BaseDato.Cursos()
        for r in range(0,len(alumn_not)):
            for c in range(0, len(alumn_not[0])):

                var = tk.StringVar()
                var.set(alumn_not[r][c])

                cell = tk.Label(
                        self.id, 
                        width=15, 
                        justify="center", 
                        bg="#ADD8E6", 
                        fg="black",
                        textvariable=var,
                        borderwidth=2, 
                        relief="groove")

                cell.grid(row=r, column=c)

class Notas(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.open_another()

    def close_it(self):
        self.id.destroy()

    def open_another(self):
        self.id = tk.Toplevel(self.parent)

        alumn_not = BaseDato.Notas()

        for r in range(0,len(alumn_not)):
            for c in range(0, len(alumn_not[0])):
                var = tk.StringVar()
                var.set(alumn_not[r][c])

                cell = tk.Label(
                        self.id, 
                        width=15, 
                        justify="center", 
                        bg="#ADD8E6", 
                        fg="black",
                        textvariable=var,
                        borderwidth=2, 
                        relief="groove")

                cell.grid(row=r, column=c)



class SQLite():
    def __init__(self):

        conn = sqlite3.connect("mantenimiento.db")
        self.c = conn.cursor()

    def Reporte(self):
        rep = []
        for rows in self.c.execute("SELECT * FROM Alumnos"):
            rep.append(rows)
             
        return rep

    def Notas(self):
        nota = []
        for rows in self.c.execute("SELECT * FROM Alumnos_Notas"):
            nota.append(rows)
    
        return nota

    def Cursos(self):
        curso = []
        for rows in self.c.execute("SELECT * FROM Cursos"):
            curso.append(rows)

        return curso

    def Contra(self):
        contra = []
        for rows in self.c.execute("SELECT codigo_AI FROM Alumnos"):
            contra.append(rows[0])

        return contra

if __name__ == "__main__":
    BaseDato = SQLite()
    app = SampleApp()
    app.mainloop()
