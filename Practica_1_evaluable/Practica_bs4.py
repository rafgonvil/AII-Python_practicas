# encoding: UTF-8

from Tkinter import *
import tkMessageBox
import sqlite3
import urllib2
from bs4 import BeautifulSoup
import datetime
import time


def almacenar():
    conn = sqlite3.connect('noticias.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")
    conn.execute('''CREATE TABLE NOTICIAS
       (TITULO TEXT NOT NULL,
       ENLACE           TEXT    NOT NULL,
       AUTOR           TEXT    NOT NULL,
       FECHA           INT    NOT NULL,
       CONTENIDO           TEXT    NOT NULL,
       VOTOSPOS           INT    NOT NULL,
       VOTOSNEG        INT NOT NULL);''')
    l = cargar_datos()
    for i in l:
        titulo,enlace,autor,fecha,contenido,votospos,votosneg=i
        conn.execute("""INSERT INTO NOTICIAS (TITULO, ENLACE, AUTOR,FECHA,CONTENIDO,VOTOSPOS,VOTOSNEG) VALUES (?,?,?,?,?,?,?)""",
                      (titulo, enlace, autor,int(fecha),contenido,int(votospos),int(votosneg)))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM NOTICIAS")
    tkMessageBox.showinfo("Base Datos",
                          "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " noticias")
    conn.close()
    
def cargar_datos():
    datos = []

    pagina = urllib2.urlopen("https://www.meneame.net/")

    for indice in range(3):

        soup = BeautifulSoup(pagina, 'html.parser')

        for noticia in soup.find_all('div', class_='news-summary'):
            titulo = noticia.find(class_='center-content').a.text
            nombre = noticia.find(class_='news-submitted').find_all('a')[1].text
            fecha = noticia.find(class_='news-submitted').find(class_='ts visible')['data-ts']
            enlace = noticia.find(class_='center-content').a['href']
            contenido = noticia.find(class_='news-content').text
            votos_p = noticia.find(class_='votes-up').text
            votos_n = noticia.find(class_='votes-down').text

            datos.append((titulo, enlace, nombre, fecha, contenido, votos_p, votos_n))

        pagina = urllib2.urlopen("https://www.meneame.net/" + '?page=' + str(indice + 2))

    return datos
    
def mostrar():
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)
    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT TITULO,AUTOR,FECHA FROM NOTICIAS")
    texto = StringVar()
    for row in cursor:
        titulo,autor,fecha = row
        lb.insert(END, titulo)
        lb.insert(END, autor)
        lb.insert(END, datetime.datetime.fromtimestamp(fecha))
        lb.insert(END, "\n")
        
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)
    
def noticia():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca una palabra a buscar en el contenido de las noticias :")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=7)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar_noticia(texto.get())) #lambda sirve para poder pasar parametros en el metodo
    buscar_button_2.pack(side=LEFT)

def command_buscar_noticia(palabra):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT TITULO,AUTOR,FECHA from NOTICIAS WHERE CONTENIDO LIKE '%"+palabra+"%';")
    for row in cursor:
        titulo, autor, fecha= row
        lb.insert(END, titulo)
        lb.insert(END, autor)
        lb.insert(END, fecha)
        lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)
    
def autor():
    t = Toplevel()
    autores = set()
    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT AUTOR FROM NOTICIAS")
    texto = StringVar()
    for row in cursor:
        print row[0]
        autores.add(row[0])
    autores=list(autores)
    w = Spinbox(t,textvariable=texto, values=autores)
    w.pack()
    buscar_button = Button(t, text="Buscar autor", command=lambda: buscar_autor(texto.get())) #lambda sirve para poder pasar parametros en el metodo
    buscar_button.pack(side=LEFT)

def buscar_autor(a):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT TITULO,AUTOR,FECHA from NOTICIAS WHERE AUTOR='"+a+"'")
    for row in cursor:
        titulo, autor, fecha = row
        lb.insert(END, titulo)
        lb.insert(END, autor)
        lb.insert(END, fecha)
        lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)  # Permite el desplazamiento
    
def fecha():
    ventana = Toplevel(width=100)

    l1 = Label(ventana, text="Introduzca una fecha (DD/MM/YYYY)  :")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=5)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar_fecha(texto.get())) #lambda sirve para poder pasar parametros en el metodo
    buscar_button_2.pack(side=LEFT)
    
def command_buscar_fecha(fe):
    fec = datetime.datetime.strptime(fe,"%d/%m/%Y")
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT TITULO,AUTOR,FECHA from NOTICIAS")
    for row in cursor:
        titulo, autor, fecha= row
        fecha1 = datetime.datetime.fromtimestamp(fecha)
        if fec < fecha1:
            lb.insert(END, titulo)
            lb.insert(END, autor)
            lb.insert(END, fecha1)
            lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)
    
    
def interfaz():

    top = Tk()
    
    menubar = Menu(top)
    datos = Menu(menubar, tearoff=0)
    datos.add_command(label="Cargar", command=almacenar)
    datos.add_command(label="Mostrar", command=mostrar)
    
    datos.add_separator()
    
    datos.add_command(label="Salir", command=top.quit)
    
    menubar.add_cascade(label="Datos", menu=datos)
    
    buscar = Menu(menubar, tearoff=0)
    
    buscar.add_command(label="Noticia", command=noticia)
    buscar.add_command(label="Autor", command=autor)
    buscar.add_command(label="Fecha", command=fecha)
    
    menubar.add_cascade(label="Buscar", menu=buscar)
    
    estadisticas = Menu(menubar, tearoff=0)
    estadisticas.add_command(label="Noticias mas valoradas")#, command=noticias_valoradas)
    estadisticas.add_command(label="Autores mas activos")#, command=autores_activos)
    menubar.add_cascade(label="Estadisticas", menu=estadisticas)
    
    top.config(menu=menubar)
    top.mainloop()
    
if __name__ == "__main__":
    interfaz()
