from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PruebaRelaciones.views.home', name='home'),
    # url(r'^PruebaRelaciones/', include('PruebaRelaciones.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$','principal.views.inicio'),
    url(r'^formdiario/$','principal.views.nuevo_diario'),
    url(r'^formautor/$','principal.views.nuevo_autor'),
)
