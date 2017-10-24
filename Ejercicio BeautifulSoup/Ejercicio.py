'''
Created on 24 oct. 2017

@author: JULIO
'''

import urllib2, re
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup

def almacenar_bd():
    conn = sqlite3.connect('productos.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS")
    conn.execute('''CREATE TABLE PRODUCTOS
       (NOMBRE TEXT PRIMARY KEY,
       LINK           TEXT    NOT NULL,
       CATEGORIA           TEXT    NOT NULL,
       PRECIO           NUMBER    NOT NULL,
       PRECIODESC        NUMBER);''')
    l = extraer_datos()
    for i in l:
        nombre,link,categoria,precio,preciodesc = i
        conn.execute("""INSERT INTO PRODUCTOS (NOMBRE, LINK, CATEGORIA,PRECIO,PRECIODESC) VALUES (?,?,?,?,?)""", (nombre,link,categoria,precio,preciodesc))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
    tkMessageBox.showinfo("Base Datos",
                          "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
def extraer_datos():
    file = urllib2.urlopen("link")
    soup = BeautifulSoup(file, 'html.parser')
    
def listar_bd():
    t = Toplevel()
    categorias = []
    conn = sqlite3.connect('productos.db')
    cursor = conn.execute("SELECT CATEGORIA FROM PRODUCTOS")
    texto = StringVar()
    for row in cursor:
        categorias.append(row[0])
        if row[0] in categorias:
            continue
    w = Spinbox(t,textvariable=texto, values=t)
    w.pack()
    buscar_button = Button(t, text="Buscar", command=lambda: buscar(texto.get())) #lambda sirve para poder pasar parametros en el metodo
    buscar_button.pack(side=LEFT)
    
def buscar(cat):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('productos.db')
    cursor = conn.execute("SELECT * from PRODUCTOS")
    for row in cursor:
        nombre, link, categoria,precio,preciodesc = row
        if cat in categoria:
            lb.insert(END, nombre)
            lb.insert(END, link)
            lb.insert(END, categoria)
            lb.insert(END, precio)
            lb.insert(END, preciodesc)
            lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)  # Permite el desplazamiento
    
    
def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar Categorias", command=almacenar_bd)
    almacenar.pack(side=LEFT)
    listar = Button(top, text="Mostrar Categorias", command=listar_bd)
    listar.pack(side=LEFT)
    top.mainloop()


if __name__ == "__main__":
    ventana_principal()

