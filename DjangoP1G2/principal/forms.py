from django.forms import ModelForm
from principal.models import Diario,Tipo_noticia, Usuario, Noticia, Autor

class DiarioForm(ModelForm):
    class Meta:
        model = Diario
        
class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario

class NoticiaForm(ModelForm):
    class Meta:
        model = Noticia
        
class AutorForm(ModelForm):
    class Meta:
        model = Autor
        
class TipoNoticiaForm(ModelForm):
    class Meta:
        model = Tipo_noticia