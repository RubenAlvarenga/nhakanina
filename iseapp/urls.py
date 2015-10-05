"""iseapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.conf import settings
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
    
    #NO MOVER DE LUGAR!!!!!!!!!!!!
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'index.html'}, name='login'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),

    url(r'^finanzas/', include('apps.finanzas.urls', namespace="finanzas", app_name='finanzas')),
    url(r'^catedras/', include('apps.catedras.urls', namespace="catedras", app_name='catedras')),
    url(r'^entidades/', include('apps.entidades.urls', namespace="entidades", app_name='entidades')),
    url(r'^autorizaciones/', include('apps.autorizaciones.urls', namespace="autorizaciones", app_name='autorizaciones')),
    url(r'^aranceles/', include('apps.aranceles.urls', namespace="aranceles", app_name='aranceles')),


]

