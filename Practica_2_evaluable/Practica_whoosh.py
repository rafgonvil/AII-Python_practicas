# encoding:utf-8
from __future__ import print_function

from Tkinter import *
import tkMessageBox

def noticia():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca una palabra a buscar en el contenido de las noticias :")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=7)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar_noticia(texto.get())) 
    buscar_button_2.pack(side=LEFT)
    
def command_buscar_noticia(palabra):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

   
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)
    
def fecha():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca una fecha (YYYYMMDD) :")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=7)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar_fecha(texto.get())) 
    buscar_button_2.pack(side=LEFT)
    
def command_buscar_fecha(texto):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

   
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)
    
def buscar_autor():
    def mostrar_cronicas(event):
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
    v.title("Búsqueda crónicas por autor")

    # Frame
    f = Frame(v)
    f.pack(side=TOP)

    # Spinbox
    autores = set()
    #seleccionar autores
    texto = StringVar()
   
   #     autores.add(row[0])
    autores=list(autores)
    w = Spinbox(v,textvariable=texto, values=autores)
    w.pack(side=LEFT)
    
    #Button
    buscar_button = Button(v, text="Buscar crónicas", command=lambda: mostrar_cronicas(texto.get()))
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
    datos_menu.add_command(label="Cargar")#, command=indexar_command)
    datos_menu.add_separator()
    datos_menu.add_command(label="Salir", command=top.quit)
    

    # Buscar
    buscar_menu = Menu(menubar_top, tearoff=0)
    menubar_top.add_cascade(label="Buscar", menu=buscar_menu)

    # Buscar/Noticia
    buscar_menu.add_command(label="Noticia", command=noticia)
    buscar_menu.add_command(label="Fecha",command=fecha)
    buscar_menu.add_command(label="Autor",command=buscar_autor)

    #Buscar/ Autor
    top.config(menu=menubar_top)
    top.mainloop()

def do_nothing():
     pass

if __name__ == '__main__':
    ventana_principal()