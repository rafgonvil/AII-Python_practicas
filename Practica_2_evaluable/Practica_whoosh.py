# encoding:utf-8
from __future__ import print_function

from Tkinter import *
import tkMessageBox



def ventana_principal():
    top = Tk()
    menubar_top = Menu(top)

    # Inicio
    inicio_menu = Menu(menubar_top, tearoff=0)
    inicio_menu.add_command(label="Indexar")#, command=indexar_command)
    inicio_menu.add_separator()
    inicio_menu.add_command(label="Salir", command=top.quit)
    menubar_top.add_cascade(label="Inicio", menu=inicio_menu)

    # Buscar
    buscar_menu = Menu(menubar_top, tearoff=0)
    menubar_top.add_cascade(label="Buscar", menu=buscar_menu)

    # Buscar/Temas
    titulo_menu = Menu(buscar_menu, tearoff=0)
    titulo_menu.add_command(label="Título")#, command=buscar_titulo_command)
    titulo_menu.add_command(label="Autor")#, command=buscar_autor_command)
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