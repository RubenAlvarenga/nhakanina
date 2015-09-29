#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.conf import settings
from django_tables2  import  A
from django.utils.html import escape
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.models import User, Group, Permission
ITEM_POR_PAGINA = 50

class ImageColumn(tables.Column):
    def render(self, value):
        #return mark_safe('<img src='+settings.MEDIA_URL+'%s height="19" width="31"/>' % escape(value))
        return mark_safe('<img src= %s height="21" width="21"/>' % escape(value.url_30x30))
class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class change_passwordColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><button type="button" class="btn btn-danger btn-xs"><span class="glyphicon '+str(self.attrs["icono"])+'"></span> '+str(self.attrs["texto"])+'</button></a>')


class UsersTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    username=tables.Column(verbose_name='usuario')
    email=tables.Column(verbose_name='e-mail')
    last_login=tables.DateTimeColumn(verbose_name="ultimo ingreso")
    is_superuser=tables.BooleanColumn(verbose_name='admin')
    is_staff=tables.BooleanColumn(verbose_name='staff')
    get_full_name = tables.Column(verbose_name='nombres', order_by =("first_name"))
    perfil=ImageColumn(verbose_name='avatar', accessor="perfil.avatar")

    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detUsuario/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updUsuario/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delUsuario/", "icono":"glyphicon-remove" }, )
    change_password = change_passwordColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"chgPassword/", "icono":"glyphicon-asterisk", "texto":"Password" }, )

    class Meta:
        model = User
        per_page=ITEM_POR_PAGINA
        exclude = ('password', 'last_name', 'first_name', 'date_joined')
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection","perfil", "id", 'username', 'email', 'get_full_name'  )


class UsersTablePDF(tables.Table):
    class Meta:
        model = User
        per_page=ITEM_POR_PAGINA
        exclude = ('password', )
        attrs = {"class": "table table-striped table-hover" }


class GroupsTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    permissions=tables.Column(verbose_name='permisos', accessor="id")    
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detGrupo/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updGrupo/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delGrupo/", "icono":"glyphicon-remove" }, )
    def render_permissions(self, record):
        return [ str(i.name) for i in record.permissions.get_queryset() ]
    class Meta:
        model = Group
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "...",  )        