# encoding: latin1

import urllib2, re
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup


# Enlace a la práctica:
# http://www.lsi.us.es/docencia/get.php?id=8986

# A - Almacenar Categorías
def extraer_datos():
    file = urllib2.urlopen("http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp")
    soup = BeautifulSoup(file, 'html.parser')
    columna_noticias = soup.find('td', width='135', valign='top')
    datos = []
    categoria_actual = 'None'
    for tr in columna_noticias.find_all('tr'):
        if tr.find(class_='TituloIndice'):
            # ha encontrado una categoría
            categoria = tr.find(class_='TituloIndice').text.strip()
            categoria_actual = categoria
            print categoria
        elif tr.find(class_='LinkIndice'):
            d = tr.find(class_='LinkIndice')
            # título link categoria
            titulo = d.text.strip()
            link = d['href'].strip()
            datos.append((titulo, link, categoria_actual))
        else:
            print 'otra cosa'
    return datos


# B - Buscar Categorías

# C - Buscar Evento

if __name__ == '__main__':
    extraer_datos()
