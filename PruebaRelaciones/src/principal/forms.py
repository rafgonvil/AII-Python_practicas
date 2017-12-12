from django.forms import ModelForm
from principal.models import Autor,Diario

class DiarioForm(ModelForm):
    class Meta:
        model = Diario
        
class AutorForm(ModelForm):
    class Meta:
        model = Autor