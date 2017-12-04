from django.db import models

# Create your models here.
class Diario(models.Model):
    nombre = models.CharField(max_length = 30)
    pais = models.CharField(max_length = 30)
    idioma = models.CharField(max_length = 30)
    def __unicode__(self):
        return self.nombre
    
    def __cmp__( self, other ) :
      if self.pais < other.pais:
        rst = -1
      elif self.pais > other.pais :
        rst = 1
      else :
        rst = 0

      return rst
    
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length = 30)
    passwd = models.CharField(max_length = 30)
    email = models.EmailField()
    nombre = models.CharField(max_length = 30)
    apellidos = models.CharField(max_length = 30)
    def __unicode__(self):
        return self.nombre
    
class Autor(models.Model):
    nombre_usuario = models.CharField(max_length = 30)
    passwd = models.CharField(max_length = 30)
    email = models.EmailField()
    nombre = models.CharField(max_length = 30)
    apellidos = models.CharField(max_length = 30)
    def __unicode__(self):
        return self.nombre

class Tipo_noticia(models.Model):
    tiponotId = models.CharField(max_length = 20,primary_key = True)
    descripcion = models.TextField()
    def __unicode__(self):
        return self.tiponotId

class Noticia(models.Model):
    #usuarios = models.ManyToManyField(Usuario,verbose_name = "usuarios interesados")
    fecha = models.DateField()
    #diario = models.OneToOneField(Diario,verbose_name = "diario")
    titular = models.CharField(max_length = 50)
    #autores = models.ManyToManyField(Autor,verbose_name = "autores")
    resumen = models.TextField()
    #tipo = models.OneToOneField(Tipo_noticia,verbose_name = "tipo noticia")
    def __unicode__(self):
        return self.titular
    