# encoding: UTF-8
from Tkinter import *
import tkMessageBox
import sqlite3
import urllib2
from bs4 import BeautifulSoup


# http://www.lsi.us.es/docencia/get.php?id=8997

def extraer_datos():
    archivo = urllib2.urlopen("http://www.delicatessin.com/es/Delicatessin")
    soup = BeautifulSoup(archivo, 'html.parser')
    # print soup.prettify()
    columna_categorias = soup.find('ul', class_="tree dhtml")
    # print columna_categorias.prettify()
    categorias = []
    for li in columna_categorias.find_all('li'):
        categoria = li.a.text
        link = li.a['href']
        categorias.append((categoria, link))

    productos_res = []
    for a in categorias:
        nombre, link = a
        link_rec = link
        while link_rec != None:
            # print 'Link:', link_rec
            archivo_aux = urllib2.urlopen(link_rec)
            soup = BeautifulSoup(archivo_aux, 'html.parser')
            productos = soup.find_all('div', class_='prod_wrap')
            for p in productos:
                nombre_link = p.find('div', class_='prod_name')
                nombre_prod = nombre_link.a.text
                link_prod = nombre_link.a['href']
                precio_producto = p.find('span', class_='product_preu')
                a = precio_producto.text.split()
                precio = a[0]
                if len(a) >= 3:
                    precio_descuento = a[2]
                else:
                    precio_descuento = None
                # print nombre_prod, link_prod, nombre, precio, precio_descuento
                productos_res.append(
                    (nombre_prod, link_prod, nombre, float(precio.replace(',', '.')),
                     None if precio_descuento is None else float(precio_descuento.replace(',', '.'))))

            # comprobar si existe siguiente página
            siguiente_p = soup.find('li', id='pagination_next')
            if siguiente_p is not None and siguiente_p.find('a'):
                link_rec = siguiente_p.a['href']
                # print 'Visitando la siguiente página'
            else:
                link_rec = None
                # print 'Fin de páginas'
    # print len(productos_res)
    return productos_res


def almacenar_bd():
    conn = sqlite3.connect('productos.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS")
    conn.execute('''CREATE TABLE PRODUCTOS
       (ID INTEGER PRIMARY KEY,
       NOMBRE TEXT NOT NULL,
       LINK           TEXT    NOT NULL,
       CATEGORIA           TEXT    NOT NULL,
       PRECIO           DOUBLE    NOT NULL,
       PRECIODESC        DOUBLE);''')

    l = extraer_datos()
    id_ = 0
    for i in l:
        nombre, link, categoria, precio, preciodesc = i
        conn.execute("""INSERT INTO PRODUCTOS (ID, NOMBRE, LINK, CATEGORIA,PRECIO,PRECIODESC) VALUES (?,?,?,?,?,?)""",
                     (id_, nombre, link, categoria, precio, preciodesc))
        id_ += 1
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
    tkMessageBox.showinfo("Base Datos",
                          "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()


def listar_bd():
    t = Toplevel()
    conn = sqlite3.connect('productos.db')
    cursor = conn.execute("SELECT CATEGORIA FROM PRODUCTOS")
    texto = StringVar()
    categorias = set()
    for row in cursor:
        categorias.add(row[0])
    categorias = list(categorias)
    w = Spinbox(t, textvariable=texto, values=categorias,width=30)
    w.pack()
    buscar_button = Button(t, text="Buscar",
                           command=lambda: buscar(texto.get()))  # lambda sirve para poder pasar parametros en el metodo
    buscar_button.pack(side=LEFT)


def buscar(cat):
    t = Toplevel()
    scrollbar = Scrollbar(t, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    lb = Listbox(t, yscrollcommand=scrollbar.set, height=30, width=100)

    conn = sqlite3.connect('productos.db')
    print "SELECT * from PRODUCTOS WHERE CATEGORIA='"+cat+"'"
    cursor = conn.execute("SELECT * from PRODUCTOS WHERE CATEGORIA='"+cat+"'")
    
    for row in cursor:
        id_, nombre, link, categoria, precio, preciodesc = row
        if cat in categoria:
            lb.insert(END, nombre)
            lb.insert(END, link)
            lb.insert(END, categoria)
            lb.insert(END, precio)
            lb.insert(END, preciodesc)
            lb.insert(END, "\n")

    conn.close()
    lb.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=lb.yview)  # Permite el desplazamiento


def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar Categorias", command=almacenar_bd)
    almacenar.pack(side=LEFT)
    listar = Button(top, text="Mostrar Categorias", command=listar_bd)
    listar.pack(side=LEFT)
    top.mainloop()


if __name__ == '__main__':
    ventana_principal()
