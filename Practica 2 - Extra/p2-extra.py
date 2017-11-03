'''
Created on 3 nov. 2017

@author: JULIO
'''
from Tkinter import *
import tkMessageBox
import sqlite3
import urllib2
from bs4 import BeautifulSoup


def almacenar_bd():
    conn = sqlite3.connect('liga.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS LIGA")
    conn.execute('''CREATE TABLE LIGA
        (JORNADA            TEXT NOT NULL,
       EQUIPOLOCAL          TEXT NOT NULL,
       GOLESLOCAL           TEXT    NOT NULL,
       AUTORESLOCAL         TEXT    NOT NULL,
       EQUIPOVISITANTE      TEXT NOT NULL,
       GOLESVISITANTE       TEXT    NOT NULL,
       AUTORESLOCAL         TEXT    NOT NULL,
       LINK        TEXT NOT NULL);''')
    #l = extraer_datos()
    for i in l:
        jornada,equipol,golesl,autoresl,equipov,golesv,autoresl,link=i
        conn.execute("""INSERT INTO LIGA (JORNADA, EQUIPOLOCAL,GOLESLOCAL, AUTORESLOCAL, EQUIPOVISITANTE,
                     GOLESVISITANTE,AUTORESVISITANTE,LINK) VALUES (?,?,?,?,?,?,?)""",
                      (jornada,equipol,golesl,autoresl,equipov,golesv,autoresl,link))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM LIGA")
    tkMessageBox.showinfo("Base Datos",
                          "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
#def extraer_datos():
    
def jornada():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca numero de jornada:")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=7)
    e1.pack(side=LEFT)

    buscar_button = Button(ventana, text="Buscar", command=lambda: command_buscar_jornada(texto.get())) #lambda sirve para poder pasar parametros en el metodo
    buscar_button.pack(side=LEFT)
    
    
def command_buscar_jornada(jornada):
    t = Toplevel()
    partidos = set()
    conn = sqlite3.connect('liga.db')
    cursor = conn.execute("SELECT EQUIPOLOCAL,EQUIPOVISITANTE FROM LIGA")
    texto = StringVar()
    for row in cursor:
        local,visitante=row
        partido = local + " - " + visitante
        print partido
        partidos.add(partido)
    partidos=list(partidos)
    w = Spinbox(t,textvariable=texto, values=autores)
    w.pack()
    buscar_button = Button(t, text="Buscar partido", command=lambda: buscar_resultado(local,visitante)) #lambda sirve para poder pasar parametros en el metodo
    buscar_button.pack(side=LEFT)
    
def buscar_resultado(local,visitante):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('liga.db')
    cursor = conn.execute("SELECT GOLESLOCAL,AUTORESLOCAL,GOLESVISITANTE,AUTORESVISITANTE from LIGA \
                            WHERE EQUIPOLOCAL='"+local+"' AND EQUIPOVISITANTE='"+visitante+"'")
    for row in cursor:
        goleslocal,autoreslocal,golesvisitante,autoresvisitante = row
        resultado = local + " " + goleslocal + " - "+visitante+" "+golesvisitante
        goles= autoreslocal + " - " + autorevisitante
        lb.insert(END, resultado)
        lb.insert(END, goles)
        lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)  # Permite el desplazamiento
    

def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar",width=8, command=almacenar_bd)
    almacenar.pack(side=LEFT)
    listar = Button(top, text="Goles", width=7, command=jornada)
    listar.pack(side=LEFT)
    top.mainloop()


if __name__ == '__main__':
    ventana_principal()