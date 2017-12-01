# Create your views here.
from principal.models import Autor,Diario,Noticia,Tipo_noticia,Usuario
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from principal.forms import AutorForm,DiarioForm,NoticiaForm,TipoNoticiaForm,UsuarioForm
from django.template import RequestContext

def nuevo_autor(request):
    if request.method == "POST":
        formulario = AutorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect("/inicio")
    else:
        formulario = AutorForm()
    return render_to_response('autorform.html',{'formulario':formulario},context_instance=RequestContext(request))

def nuevo_diario(request):
    if request.method == "POST":
        formulario = DiarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect("/inicio")
    else:
        formulario = DiarioForm()
    return render_to_response('diarioform.html',{'formulario':formulario},context_instance=RequestContext(request))

def nueva_noticia(request):
    if request.method == "POST":
        formulario = NoticiaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect("/inicio")
    else:
        formulario = NoticiaForm()
    return render_to_response('noticiaform.html',{'formulario':formulario},context_instance=RequestContext(request))

def nuevo_tiponoticia(request):
    if request.method == "POST":
        formulario = TipoNoticiaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect("/inicio")
    else:
        formulario = TipoNoticiaForm()
    return render_to_response('tiponoticiaform.html',{'formulario':formulario},context_instance=RequestContext(request))
            
def nuevo_usuario(request):
    if request.method == "POST":
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect("/inicio")
    else:
        formulario = UsuarioForm()
    return render_to_response('usuarioform.html',{'formulario':formulario},context_instance=RequestContext(request))

def diarios(request):
    pass

#def login(request):
    