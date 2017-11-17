# encoding:utf-8
from __future__ import print_function

from Tkinter import *
import tkMessageBox

def extraer_datos():
    """
    Extraer todos los datos utilizando BS4 y devolverlos
    """

def cargar_command():
    """
    1 - Extraer datos de la web con BS4
    2 - Guardar los datos con Whoosh
    3 - Notificar con una ventana emergente
    """
    pass


def buscar_1():
    pass


def buscar_2():
    pass


def buscar_3():
    pass


def ventana_principal():
    top = Tk()
    menubar_top = Menu(top)

    # Datos
    datos_menu = Menu(menubar_top, tearoff=0)
    menubar_top.add_cascade(label="Datos", menu=datos_menu)
    datos_menu.add_command(label="Cargar", command=cargar_command)
    datos_menu.add_separator()
    datos_menu.add_command(label="Salir", command=top.quit)

    # Buscar
    buscar_menu = Menu(menubar_top, tearoff=0)
    menubar_top.add_cascade(label="Buscar", menu=buscar_menu)

    # Buscar/Comandos
    buscar_menu.add_command(label="Noticia", command=buscar_1)
    buscar_menu.add_command(label="Fecha", command=buscar_2)
    buscar_menu.add_command(label="Autor", command=buscar_3)

    # Buscar/ Autor
    top.config(menu=menubar_top)
    top.mainloop()


if __name__ == '__main__':
    ventana_principal()
