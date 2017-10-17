from Tkinter import *
import tkMessageBox
import P1
import sqlite3
from compileall import expand_args


def almacenar():
    fichero = "noticias"
    if P1.abrir_url("http://www.us.es/rss/feed/portada", fichero):
        l = P1.extraer_lista(fichero)
    if l:
        P1.almacenar(l)
    tkMessageBox.showinfo("Info", "BD creada correctamente")
    
def listar():
    t = Tk()
    scrollbar = Scrollbar(t, orient= VERTICAL)
    scrollbar.pack(side=RIGHT,fill=Y)
    
    lb = Listbox(t,yscrollcommand = scrollbar.set,height=30,width=100)
    
    conn = sqlite3.connect('noticias.db')
    cursor = conn.execute("SELECT * from NOTICIAS")
    for row in cursor:  
        lb.insert(1, row[0])
        lb.insert(2, row[1])
        lb.insert(3, row[2])
        lb.insert(4, "\n")
       
    conn.close() 
    lb.pack( side = LEFT, fill = BOTH )
    scrollbar.config(command=lb.yview)     #Permite el desplazamiento 
    top.mainloop()
    
    
top = Tk()

almacenar_button = Button(top, text="Almacenar", command=almacenar)
listar_button = Button(top, text="Listar", command=listar)
buscar_button = Button(top, text="Buscar")

almacenar_button.pack(side='left')
listar_button.pack(side='left')
buscar_button.pack(side='left')

top.mainloop()
