from django.db import models
from django.conf import settings

class Diario(models.Model):
    nombre = models.CharField(max_length=30)
    pais = models.CharField(max_length=30)
    idioma = models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
    
class Autor(models.Model):
    nombre_usuario = models.CharField(max_length=30)
    passwd = models.CharField(max_length=30)
    diario = models.ForeignKey(Diario)
    def __unicode__(self):
        return self.nombre