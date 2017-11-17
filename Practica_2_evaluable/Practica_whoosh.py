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

dirindex = "Index_productos"

def extraer_datos():
    pass

def cargar_command():
    datos = extraer_datos("http://www.delicatessin.com/es/Delicatessin", 1)

    if datos:  # Comprueba si contiene algo
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)
    else:
        print("No se ha extraido ningun dato")
        return

    ix_temas = create_in(dirindex, schema=get_schema_temas())
    writer = ix_temas.writer()

    productos = 0
    for dato in datos:
        marca2,nombre2,descripcion2,url_imagen2,caracteristicas2 = dato
        writer.add_document(marca=marca2, nombre=nombre2, descripcion=descripcion2,
                            url_imagen=url_imagen2, caracteristicas=caracteristicas2)
        productos += 1

    writer.commit()
    tkMessageBox.showinfo("Indexar", "Se han indexado {} productos".format(productos))
    
def get_schema_producto():
    return Schema(marca=TEXT(stored=True), nombre=TEXT(stored=True), descripcion=TEXT(stored=True),
                  url_imagen=TEXT(stored=True), caracteristicas=KEYWORD(stored=True))

def descripcion():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca una/varias palabra/s a buscar en la descripcion del producto :")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=7)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar_descripcion(texto.get())) 
    buscar_button_2.pack(side=LEFT)
    
def command_buscar_descripcion(texto):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lbox = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)
    lbox.delete(0, END)  # borra toda la lista
    ix = open_dir(dirindex)
    with ix.searcher() as searcher:
        query = QueryParser("descripcion", ix.schema).parse(unicode(texto))
        results = searcher.search(query)
        for r in results:
            lbox.insert(END, r['marca'])
            lbox.insert(END, r['nombre'])
            lbox.insert(END, r['url_imagen'])
            lbox.insert(END, '')
   
    lbox.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)
    
def caracteristica():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca una caracteristica :")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=7)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar_caracteristica(texto.get())) 
    buscar_button_2.pack(side=LEFT)
    
def command_buscar_caracteristica(texto):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lbox = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)
    lbox.delete(0, END)  # borra toda la lista
    ix = open_dir(dirindex)
    with ix.searcher() as searcher:
        query = QueryParser("caracteristicas", ix.schema).parse(unicode(texto))
        results = searcher.search(query)
        for r in results:
            lbox.insert(END, r['marca'])
            lbox.insert(END, r['nombre'])
            lbox.insert(END, r['url_imagen'])
            lbox.insert(END, '')
   
    lbox.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)
    
def marca():
    def mostrar_productos(palabra):
        lbox.delete(0, END)  # borra toda la lista
        ix = open_dir(dirindex)
        with ix.searcher() as searcher:
            query = QueryParser("marca", ix.schema).parse(unicode(palabra))
            results = searcher.search(query)
            for r in results:
                lbox.insert(END, r['titulo'])
                lbox.insert(END, r['autor'])
                lbox.insert(END, r['fecha'])
                lbox.insert(END, '')

    # Window
    v = Toplevel()
    v.title("Búsqueda crónicas por autor")

    # Frame
    f = Frame(v)
    f.pack(side=TOP)

    # Spinbox
    autores = set()
    texto = StringVar()
    ix = open_dir(dirindex)
    with ix.searcher() as searcher:
        query = QueryParser("marca", ix.schema)
        #print (query)
        print (list(searcher.lexicon("marca")))  
        #autores.add(row[0])
        autores=list(autores)
        
    w = Spinbox(f,textvariable=texto, values=autores)
    w.pack(side=LEFT)
    
    #Button
    buscar_button = Button(f, text="Buscar crónicas", command=lambda: mostrar_productos(texto.get()))
    buscar_button.pack(side=LEFT)

    # ScrollBar
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)

    # ListBox
    lbox = Listbox(v, yscrollcommand=sc.set,width=50)
    lbox.pack(side=BOTTOM, fill=BOTH)
    sc.config(command=lbox.yview)
    
    
def ventana_principal():
    top = Tk()
    menubar_top = Menu(top)

    # Datos
    datos_menu = Menu(menubar_top, tearoff=0)
    menubar_top.add_cascade(label="Datos", menu=datos_menu)
    datos_menu.add_command(label="Cargar",command=cargar_command)
    datos_menu.add_separator()
    datos_menu.add_command(label="Salir", command=top.quit)
    

    # Buscar
    buscar_menu = Menu(menubar_top, tearoff=0)
    menubar_top.add_cascade(label="Buscar", menu=buscar_menu)

    # Buscar/Noticia
    buscar_menu.add_command(label="Descripcion", command=descripcion)
    buscar_menu.add_command(label="Caracteristica",command=caracteristica)
    buscar_menu.add_command(label="Marca",command=marca)

    #Buscar/ Autor
    top.config(menu=menubar_top)
    top.mainloop()

if __name__ == '__main__':
    ventana_principal()