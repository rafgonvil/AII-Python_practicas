# encoding:utf-8
from __future__ import print_function

from Tkinter import *
import tkMessageBox
from bs4 import BeautifulSoup
import urllib2
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser

dirindex = "Index_temas"


def extraer_datos(url):
    archivo = urllib2.urlopen(url)
    soup = BeautifulSoup(archivo, 'html.parser')

    enlace_padre = "https://foros.derecho.com/"
    datos = []

    for tema in soup.find_all("li", class_="threadbit"):
        # título y enlace al tema
        titulo_object = tema.find('a', class_="title")
        titulo = titulo_object.text
        enlace = enlace_padre + titulo_object["href"]

        # autor
        autor_object = tema.find("a", class_="username")
        nombre_autor = autor_object.text
        enlace_autor = enlace_padre + autor_object["href"]

        # fecha
        fecha_text = tema.find("span", class_='label').text
        fecha = fecha_text.split()[-2]

        # respuestas y visitas
        thread_stats = tema.find("ul", class_="threadstats")
        respuestas = thread_stats.a.text
        visitas = thread_stats.find_all("li")[1].text[9:]

        # Introducir datos
        datos.append(
            {"titulo": titulo, "enlace": enlace, "autor": nombre_autor, "enlace_autor": enlace_autor, "fecha": fecha,
             "respuestas": respuestas, "visitas": visitas})

    siguiente_pagina = soup.find("a", rel="next")

    if siguiente_pagina is not None:
        print("Accediendo a la siguiente página")
        datos.extend(extraer_datos(enlace_padre + siguiente_pagina["href"]))

    return datos


def indexar_command():
    datos = extraer_datos("http://foros.derecho.com/foro/20-Derecho-Civil-General")

    if datos:  # Comprueba si contiene algo
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)
    else:
        print("No se ha extraido ningun dato")
        return

    ix_temas = create_in(dirindex, schema=get_schema_temas())
    writer = ix_temas.writer()

    temas_i = 0
    for dato in datos:
        writer.add_document(titulo=dato["titulo"], enlace=dato["enlace"], autor=dato["autor"],
                            enlace_autor=dato["enlace_autor"], fecha=dato["fecha"], respuestas=dato["respuestas"],
                            visitas=dato["visitas"])
        temas_i += 1

    respuestas_i = 0
    tkMessageBox.showinfo("Indexar", "Se han indexado {} Temas y {} Respuestas".format(temas_i, respuestas_i))


def get_schema_temas():
    return Schema(titulo=TEXT(stored=True), enlace=TEXT(stored=True), autor=TEXT(stored=True),
                  enlace_autor=TEXT(stored=True), fecha=TEXT(stored=True), respuestas=TEXT(stored=True),
                  visitas=TEXT(stored=True))


def ventana_principal():
    top = Tk()
    menubar_top = Menu(top)

    # Inicio
    inicio_menu = Menu(menubar_top, tearoff=0)
    inicio_menu.add_command(label="Indexar", command=do_nothing)
    inicio_menu.add_separator()
    inicio_menu.add_command(label="Salir", command=top.quit)
    menubar_top.add_cascade(label="Inicio", menu=inicio_menu)

    # Buscar
    buscar_menu = Menu(menubar_top, tearoff=0)
    menubar_top.add_cascade(label="Buscar", menu=buscar_menu)

    # Buscar/Temas
    titulo_menu = Menu(buscar_menu, tearoff=0)
    titulo_menu.add_command(label="Título", command=do_nothing)
    titulo_menu.add_command(label="Autor", command=do_nothing)
    buscar_menu.add_cascade(label="Temas", menu=titulo_menu)

    # Buscar/Respuestas
    respuestas_menu = Menu(buscar_menu, tearoff=0)
    respuestas_menu.add_command(label="Texto", command=do_nothing)
    buscar_menu.add_cascade(label="Respuestas", menu=respuestas_menu)

    top.config(menu=menubar_top)
    top.mainloop()


def do_nothing():
    pass


if __name__ == '__main__':
    indexar_command()
    # ventana_principal()
