from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoP1G2.views.home', name='home'),
    # url(r'^DjangoP1G2/', include('DjangoP1G2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^/formdiario$','principal.views.nuevo_diario'),
    url(r'^/formusuario$','principal.views.nuevo_usuario'),
    url(r'^/formnoticia$','principal.views.nueva_noticia'),
    url(r'^/formautor$','principal.views.nuevo_autor'),
    url(r'^/formtiponoticia$','principal.views.nuevo_tiponoticia'),
    url(r'^/diarios$','principal.views.diarios'),
    url(r'^/login$','principal.views.login'),
    
)
