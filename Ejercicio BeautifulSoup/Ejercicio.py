'''
Created on 24 oct. 2017

@author: JULIO
'''

import urllib2, re
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup

def almacenar_bd():
    conn = sqlite3.connect('productos.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS")
    conn.execute('''CREATE TABLE PRODUCTOS
       (NOMBRE TEXT PRIMARY KEY,
       LINK           TEXT    NOT NULL,
       CATEGORIA           TEXT    NOT NULL,
       PRECIO           DOUBLE    NOT NULL,
       PRECIODESC        DOUBLE NOT NULL);''')
    l = extraer_datos()
    for i in l:
        nombre,link,categoria,precio,preciodesc = i
        conn.execute("""INSERT INTO PRODUCTOS (NOMBRE, LINK, CATEGORIA,PRECIO,PRECIODESC) VALUES (?,?,?,?,?)""", (nombre,link,categoria,precio,preciodesc))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
    tkMessageBox.showinfo("Base Datos",
                          "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
def extraer_datos():
    file = urllib2.urlopen("http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp")
    soup = BeautifulSoup(file, 'html.parser')
    print soup.find_all().__doc__
