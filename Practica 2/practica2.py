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
    print soup.find_all().__doc__


# B - Buscar Categorías

# C - Buscar Evento

if __name__ == '__main__':
    extraer_datos()
