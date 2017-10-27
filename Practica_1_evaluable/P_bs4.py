# encoding: UTF-8

from Tkinter import *
import tkMessageBox
import sqlite3
import urllib2
from bs4 import BeautifulSoup


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

            datos.append((titulo, nombre, fecha, enlace, contenido, votos_p, votos_n))

        pagina = urllib2.urlopen("https://www.meneame.net/" + '?page=' + str(indice + 2))

    return datos


def almacenar():
    conn = sqlite3.connect('noticias.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")
    conn.execute('''CREATE TABLE NOTICIAS
       (TITULO TEXT NOT NULL,
       ENLACE           TEXT    NOT NULL,
       AUTOR           TEXT    NOT NULL,
       FECHA           TEXT    NOT NULL,
       CONTENIDO           TEXT    NOT NULL,
       VOTOSPOS           INT    NOT NULL,
       VOTOSNEG        INT NOT NULL);''')
    l = cargar_datos()
    for i in l:
        titulo, enlace, autor, fecha, contenido, votospos, votosneg = i
        conn.execute(
            """INSERT INTO NOTICIAS (TITULO, ENLACE, AUTOR,FECHA,CONTENIDO,VOTOSPOS,VOTOSNEG) VALUES (?,?,?,?,?,?,?)""",
            (titulo, enlace, autor, fecha, contenido, int(votospos), int(votosneg)))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM NOTICIAS")
    tkMessageBox.showinfo("Base Datos",
                          "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " noticias")
    conn.close()


def mostrar():
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)
    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT TITULO,AUTOR,FECHA FROM NOTICIAS")
    texto = StringVar()
    for row in cursor:
        titulo, autor, fecha = row
        lb.insert(END, titulo)
        lb.insert(END, autor)
        lb.insert(END, fecha)
        lb.insert(END, "\n")

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

    buscar.add_command(label="Noticia")  # , command=noticia)
    buscar.add_command(label="Autor")  # , command=autor)
    buscar.add_command(label="Fecha")  # , command=fecha)

    menubar.add_cascade(label="Buscar", menu=buscar)

    estadisticas = Menu(menubar, tearoff=0)
    estadisticas.add_command(label="Noticias mas valoradas")  # , command=noticias_valoradas)
    estadisticas.add_command(label="Autores mas activos")  # , command=autores_activos)
    menubar.add_cascade(label="Estadisticas", menu=estadisticas)

    top.config(menu=menubar)
    top.mainloop()


if __name__ == "__main__":
    interfaz()

