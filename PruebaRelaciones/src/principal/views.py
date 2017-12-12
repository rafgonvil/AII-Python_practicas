from principal.models import Autor,Diario
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from principal.forms import AutorForm,DiarioForm
from django.template import RequestContext
from django.http import HttpResponse


def nuevo_diario(request):
    if request.method == "POST":
        formulario = DiarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect("/inicio")
    else:
        formulario = DiarioForm()
    return render_to_response('enviar.html',{'formulario':formulario},context_instance=RequestContext(request))


def nuevo_autor(request):
    if request.method == "POST":
        formulario = AutorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect("/inicio")
    else:
        formulario = AutorForm()
    return render_to_response('enviar.html',{'formulario':formulario},context_instance=RequestContext(request))

def inicio(request):
    return render_to_response('inicio.html')