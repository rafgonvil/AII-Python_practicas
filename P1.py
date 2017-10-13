'''
Created on 13 oct. 2017

@author: JULIO
'''
# encoding: utf-8

import urllib, re
import os.path
import sqlite3


def almacenar_lineas(titulo, link, fecha, conn):
    conn.execute("INSERT INTO NOTICIAS (TITULO,LINK,FECHA) VALUES ('%s','%s','%s')" % (titulo, link, fecha));
    conn.commit()


def extraer_lista(file):
    f = open(file, "r")
    s = f.read()
    l = re.findall(
        r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>',
        s)
    f.close()
    return l


def almacenar(l):
    conn = sqlite3.connect('noticias.db')
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")
    conn.execute('''CREATE TABLE IF NOT EXISTS NOTICIAS
         (TITULO TEXT PRIMARY KEY     NOT NULL,
         LINK           TEXT    NOT NULL,
         FECHA          TEXT    NOT NULL);''')
    for t in l:
        titulo, link, categoria, fecha = t
        almacenar_lineas(titulo, link, fecha, conn)
    conn.close()


def abrir_url(url, file):
    try:
        if os.path.exists(file):
            f = urllib.urlretrieve(url, file)
        return file
    except:
        print  "Error al conectarse a la pagina"
        return None


def buscar_fecha(l):
    n = raw_input("Introduzca el dia (dd-mm-aaaa):")
    fecha = re.match(r'(\d\d)-(\d\d)-(\d\d\d\d)', n)
    if not fecha:
        print "Formato de fecha incorrecto"
        return
    enc = False
    for t in l:
        if fecha.groups() == formatear_fecha(t[3]):
            print "Titulo:", unicode(t[0])
            print "Link:", t[1]
            print "Fecha: %2s/%2s/%4s\n" % formatear_fecha(t[3])
            enc = True
    if not enc:
        print "No hay noticias para ese mes"


def formatear_fecha(s):
    meses = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
             'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dic': '12'}
    fecha = re.match(r'.*(\d\d)\s*(.{3})\s*(\d{4}).*', s)
    l = list(fecha.groups())
    l[1] = meses[l[1]]
    return tuple(l)


if __name__ == "__main__":
    fichero = "noticias"
    if abrir_url("http://www.us.es/rss/feed/portada", fichero):
        l = extraer_lista(fichero)
    if l:
        almacenar(l)
        # buscar_fecha(l)
