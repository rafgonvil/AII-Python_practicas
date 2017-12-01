from django.db import models
from pattern.db import primary_key

# Create your models here.
class Diario(models.Model):
    nombre = models.CharField(max_length = 30)
    pais = models.CharField(max_length = 30)
    idioma = models.CharField(max_length = 30)
    
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length = 30)
    passwd = models.CharField(max_length = 30)
    email = models.EmailField()
    nombre = models.CharField(max_length = 30)
    apellidos = models.CharField(max_length = 30)
    
class Autor(models.Model):
    nombre_usuario = models.CharField(max_length = 30)
    passwd = models.CharField(max_length = 30)
    email = models.EmailField()
    nombre = models.CharField(max_length = 30)
    apellidos = models.CharField(max_length = 30)

class Tipo_noticia(models.Model):
    tiponotId = models.CharField(max_length = 20,primary_key = True)
    descripcion = models.TextField()

class Noticia(models.Model):
    usuarios = models.ManyToManyField(Usuario,verbose_name = "usuarios interesados")
    fecha = models.DateField()
    diario = models.OneToOneField(Diario,verbose_name = "diario")
    titular = models.CharField(max_length = 50)
    autores = models.ManyToManyField(Autor,verbose_name = "autores")
    resumen = models.TextField()
    tipo = models.OneToOneField(Tipo_noticia,verbose_name = "tipo noticia")
    

    
