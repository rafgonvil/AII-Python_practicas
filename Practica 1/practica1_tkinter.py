from Tkinter import *
import tkMessageBox
import P1
import sqlite3
from compileall import expand_args


def almacenar():
    fichero = "noticias"
    if P1.abrir_url("http://www.us.es/rss/feed/portada", fichero):
        l = P1.extraer_lista(fichero)
    if l:
        P1.almacenar(l)
    tkMessageBox.showinfo("Info", "BD creada correctamente")


def listar():
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT * from NOTICIAS")
    for row in cursor:
        lb.insert(END, row[0])
        lb.insert(END, row[1])
        lb.insert(END, row[2])
        lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)  # Permite el desplazamiento


def command_buscar(mes):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT * from NOTICIAS")
    for row in cursor:
        titulo, link, fecha = row
        if mes in str(fecha):
            lb.insert(END, titulo)
            lb.insert(END, link)
            lb.insert(END, fecha)
            lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)  # Permite el desplazamiento


def buscar():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca el mes (Xxx):")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=5)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar(texto.get()))
    buscar_button_2.pack(side=LEFT)


top = Tk()

almacenar_button = Button(top, text="Almacenar", command=almacenar)
listar_button = Button(top, text="Listar", command=listar)
buscar_button = Button(top, text="Buscar", command=buscar)

almacenar_button.pack(side='left')
listar_button.pack(side='left')
buscar_button.pack(side='left')

top.mainloop()
