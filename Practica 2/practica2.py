# encoding: UTF-8
from Tkinter import *
import tkMessageBox
import sqlite3
import urllib2
from bs4 import BeautifulSoup

# Enlace a la práctica:
# http://www.lsi.us.es/docencia/get.php?id=8986

def almacenar():
    conn = sqlite3.connect('categorias.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS CATEGORIAS")
    conn.execute('''CREATE TABLE CATEGORIAS
       (TITULO TEXT PRIMARY KEY,
       LINK           TEXT    NOT NULL,
       CATEGORIA        TEXT NOT NULL);''')
    l = extraer_datos()
    for i in l:
        titulo,link,categoria=i
        conn.execute("""INSERT INTO CATEGORIAS (TITULO, LINK, CATEGORIA) VALUES (?,?,?)""", (titulo, link, categoria))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM CATEGORIAS")
    tkMessageBox.showinfo("Base Datos",
                          "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()


# A - Almacenar Categorías

def extraer_datos():
 
    file = urllib2.urlopen("http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp")
    soup = BeautifulSoup(file, 'html.parser')
    columna_noticias = soup.find('td', width='135', valign='top')
    datos = []
    categoria_actual = 'None'
    for tr in columna_noticias.find_all('tr'):
        if tr.find(class_='TituloIndice'):
            # ha encontrado una categor�a
            categoria = tr.find(class_='TituloIndice').text.strip()
            categoria_actual = categoria
            print categoria
 
        elif tr.find(class_='LinkIndice'):
            d = tr.find(class_='LinkIndice')
            # t�tulo link categoria
            titulo = d.text.strip()
            link = d['href'].strip()
            datos.append((titulo, link, categoria_actual))
            
        else:
            print 'otra cosa'
 
    return datos
 
    
# B - Buscar Categorías

def command_buscar(cat):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('categorias.db')
    cursor = conn.execute("SELECT * from CATEGORIAS")
    for row in cursor:
        titulo, link, categoria = row
        if cat in categoria:
            lb.insert(END, titulo)
            lb.insert(END, link)
            lb.insert(END, categoria)
            lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)  # Permite el desplazamiento


def buscar_categoria():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca la categoria :")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=5)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar(texto.get())) #lambda sirve para poder pasar parametros en el metodo
    buscar_button_2.pack(side=LEFT)

# C - Buscar Evento

def buscar_evento():
    ventana = Toplevel()

    l1 = Label(ventana, text="Introduzca palabra a buscar en el evento :")
    l1.pack(side=LEFT)

    texto = StringVar()
    e1 = Entry(ventana, textvariable=texto, bd=7)
    e1.pack(side=LEFT)

    buscar_button_2 = Button(ventana, text="Buscar", command=lambda: command_buscar_evento(texto.get())) #lambda sirve para poder pasar parametros en el metodo
    buscar_button_2.pack(side=LEFT)

def command_buscar_evento(palabra):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    file = urllib2.urlopen("http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp")
    soup = BeautifulSoup(file, 'html.parser')
    descripcion = soup.find_all(class_="Destacamos")
    encabezado = soup.find_all(class_="Sala")
    for i in descripcion:
        texto = i.get_text()
        a=0;
        if palabra in texto:
            fecha= encabezado[a].text
            titulo=i.strong.text
            lb.insert(END, titulo)
            lb.insert(END, fecha)
            lb.insert(END, "\n")

    
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)

top = Tk()

almacenar_button = Button(top, text="Almacenar",command=almacenar)
buscar_categoria_button = Button(top, text="Buscar Categoria", command=buscar_categoria)
buscar_evento_button = Button(top, text="Buscar Evento", command=buscar_evento)

almacenar_button.pack(side='left')
buscar_categoria_button.pack(side='left')
buscar_evento_button.pack(side='left')

top.mainloop()
