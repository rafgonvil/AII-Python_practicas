from Tkinter import *
import tkMessageBox
import P1


def almacenar():
    fichero = "noticias"
    if P1.abrir_url("http://www.us.es/rss/feed/portada", fichero):
        l = P1.extraer_lista(fichero)
    if l:
        P1.almacenar(l)
    tkMessageBox.showinfo("Info", "BD creada correctamente")


top = Tk()

almacenar_button = Button(top, text="Almacenar", command=almacenar)
listar_button = Button(top, text="Listar")
buscar_button = Button(top, text="Buscar")

almacenar_button.pack(side='left')
listar_button.pack(side='left')
buscar_button.pack(side='left')

top.mainloop()
