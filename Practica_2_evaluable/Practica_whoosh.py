# encoding:utf-8
from __future__ import print_function

from Tkinter import *
import tkMessageBox

























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
    titulo_menu = Menu(buscar_menu, tearoff=0)
    buscar_menu.add_cascade(label="Noticias", menu=titulo_menu)
    titulo_menu.add_command(label="Título")#, command=buscar_titulo_command)
    titulo_menu.add_command(label="Autor")#, command=buscar_autor_command)


    # Buscar/Fecha
    respuestas_menu = Menu(buscar_menu, tearoff=0)
    buscar_menu.add_cascade(label="Fecha", menu=respuestas_menu)
    respuestas_menu.add_command(label="Texto", command=do_nothing)

    #Buscar/ Autor
    top.config(menu=menubar_top)
    top.mainloop()

def do_nothing():
     pass

if __name__ == '__main__':
    ventana_principal()