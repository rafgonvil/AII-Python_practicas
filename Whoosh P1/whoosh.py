'''
Created on 10 nov. 2017

@author: JULIO
'''

from Tkinter import *
import tkMessageBox
import os
#from whoosh.index import create_in, open_dir
#from whoosh.fields import Schema, TEXT, KEYWORD
#from whoosh.qparser import QueryParser

    


def interfaz():

    top = Tk()
    
    menubar = Menu(top)
    inicio = Menu(menubar, tearoff=0)
    inicio.add_command(label="Indexar")#, command=indexar)
    inicio.add_command(label="Salir", command=top.quit)
    
    menubar.add_cascade(label="Datos", menu=inicio)
    
    buscar = Menu(menubar, tearoff=0)
    
    temas = Menu(menubar, tearoff=0)
    temas.add_command(label="Titulo")#, command=noticias_valoradas)
    temas.add_command(label="Autor")#, command=autores_activos)
    buscar.add_cascade(label="Temas", menu=temas)
    respuestas = Menu(menubar, tearoff=0)
    respuestas.add_command(label="Texto")
    buscar.add_cascade(label="Respuestas", menu=respuestas)
    
    menubar.add_cascade(label="Buscar", menu=buscar)
    
    top.config(menu=menubar)
    top.mainloop()
    
if __name__ == "__main__":
    interfaz()
