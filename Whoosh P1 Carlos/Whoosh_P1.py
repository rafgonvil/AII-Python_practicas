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
max_paginas = 1


def extraer_datos(url, pagina_actual, maximo_paginas):
    archivo = urllib2.urlopen(url)
    soup = BeautifulSoup(archivo, 'html.parser')

    enlace_padre = "https://foros.derecho.com/"
    datos = []

    for tema in soup.find_all("li", class_="threadbit"):
        # título y enlace al tema
        titulo_object = tema.find('a', class_="title")
        titulo = unicode(titulo_object.text.strip())
        enlace = unicode(enlace_padre + titulo_object["href"].strip())
        
        # tema abierto para añadir respuestas, cogiendo HASTA EL TEMA (no deberia)
        archivo2 = urllib2.urlopen(enlace)
        soup2 = BeautifulSoup(archivo2, 'html.parser')
        
        respuestas = soup2.find_all('div',class_="postbody")
        for r in respuestas:
            r.text
        fechas = soup2.find_all("span",class_='date')
        for fe in fechas:
            fecha_resp = fe.text.split(',')[0]
        nombres = soup2.find_all('a',class_='username')
        for n in nombres:
            nombre = n.strong.text
            link = enlace_padre + n.get('href')
            print (link)
        
        # autor
        autor_object = tema.find("a", class_="username")
        nombre_autor = unicode(autor_object.text.strip())
        enlace_autor = unicode(enlace_padre + autor_object["href"].strip())

        # fecha
        fecha_text = unicode(tema.find("span", class_='label').text.strip())
        fecha = unicode(fecha_text.split()[-2].strip())

        # respuestas y visitas
        thread_stats = tema.find("ul", class_="threadstats")
        respuestas = unicode(thread_stats.a.text.strip())
        visitas = unicode(thread_stats.find_all("li")[1].text[9:].strip())

        # Introducir datos
        datos.append(
            {"titulo": titulo, "enlace": enlace, "autor": nombre_autor, "enlace_autor": enlace_autor, "fecha": fecha,
             "respuestas": respuestas, "visitas": visitas})

    siguiente_pagina = soup.find("a", rel="next")

    # Navegando a las siguientes páginas por recursividad
    if pagina_actual < maximo_paginas and siguiente_pagina is not None:
        print("Accediendo a la página", pagina_actual + 1)
        datos.extend(extraer_datos(enlace_padre + siguiente_pagina["href"], pagina_actual + 1, maximo_paginas))

    return datos


def indexar_command():
    datos = extraer_datos("http://foros.derecho.com/foro/20-Derecho-Civil-General", 1, max_paginas)

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

    writer.commit()

    respuestas_i = 0
    tkMessageBox.showinfo("Indexar", "Se han indexado {} Temas y {} Respuestas".format(temas_i, respuestas_i))


def buscar_titulo_command():
    def mostrar_lista_temas(event):
        lbox.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindex)
        with ix.searcher() as searcher:
            query = QueryParser("titulo", ix.schema).parse(unicode(en.get()))
            results = searcher.search(query)
            for r in results:
                lbox.insert(END, r['titulo'])
                lbox.insert(END, r['autor'])
                lbox.insert(END, r['fecha'])
                lbox.insert(END, '')

    # Window
    v = Toplevel()
    v.title("Búsqueda temas por título")

    # Frame
    f = Frame(v)
    f.pack(side=TOP)

    # Label
    lbl = Label(f, text="Introduzca un título:")
    lbl.pack(side=LEFT)

    # Entry
    en = Entry(f,width=20)
    en.bind("<Return>", mostrar_lista_temas)
    en.pack(side=LEFT)

    # ScrollBar
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)

    # ListBox
    lbox = Listbox(v, yscrollcommand=sc.set,width=50)
    lbox.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lbox.yview)

def buscar_autor_command():
    def mostrar_lista_temas(event):
        lbox.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindex)
        with ix.searcher() as searcher:
            query = QueryParser("autor", ix.schema).parse(unicode(en.get()))
            results = searcher.search(query)
            for r in results:
                lbox.insert(END, r['titulo'])
                lbox.insert(END, r['autor'])
                lbox.insert(END, r['fecha'])
                lbox.insert(END, '')

    # Window
    v = Toplevel()
    v.title("Búsqueda temas por título")

    # Frame
    f = Frame(v)
    f.pack(side=TOP)

    # Label
    lbl = Label(f, text="Introduzca un título:")
    lbl.pack(side=LEFT)

    # Entry
    en = Entry(f,width=20)
    en.bind("<Return>", mostrar_lista_temas)
    en.pack(side=LEFT)

    # ScrollBar
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)

    # ListBox
    lbox = Listbox(v, yscrollcommand=sc.set,width=50)
    lbox.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lbox.yview)

def get_schema_temas():
    return Schema(titulo=TEXT(stored=True), enlace=TEXT(stored=True), autor=TEXT(stored=True),
                  enlace_autor=TEXT(stored=True), fecha=TEXT(stored=True), respuestas=TEXT(stored=True),
                  visitas=TEXT(stored=True))

def get_schema_respuestas():
    return Schema(titulo=TEXT(stored=True), texto=TEXT(stored=True), autor=TEXT(stored=True),
                  enlace_autor=TEXT(stored=True), fecha=TEXT(stored=True))

def ventana_principal():
    top = Tk()
    menubar_top = Menu(top)

    # Inicio
    inicio_menu = Menu(menubar_top, tearoff=0)
    inicio_menu.add_command(label="Indexar", command=indexar_command)
    inicio_menu.add_separator()
    inicio_menu.add_command(label="Salir", command=top.quit)
    menubar_top.add_cascade(label="Inicio", menu=inicio_menu)

    # Buscar
    buscar_menu = Menu(menubar_top, tearoff=0)
    menubar_top.add_cascade(label="Buscar", menu=buscar_menu)

    # Buscar/Temas
    titulo_menu = Menu(buscar_menu, tearoff=0)
    titulo_menu.add_command(label="Título", command=buscar_titulo_command)
    titulo_menu.add_command(label="Autor", command=buscar_autor_command)
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
    ventana_principal()
