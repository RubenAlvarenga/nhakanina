#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from .models import Persona, Alumno
from django.utils.safestring import mark_safe
from django.conf import settings
from  django_tables2  import  A

from django.utils.html import escape
ITEM_POR_PAGINA = 50

class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class PersonasTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )    
    get_full_name = tables.Column(verbose_name='nombres', order_by =("apellido1"))
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detPersona/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updPersona/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delPersona/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = Persona
        exclude = ('apellido1', 'apellido2', 'nombre1', 'nombre2')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "get_full_name", "cedula", "...", "ver", "editar", "borrar" )

class PersonasTablePDF(tables.Table):
    get_full_name = tables.Column(verbose_name='nombres', order_by =("apellido1"))
    class Meta:
        model = Persona
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("id", "get_full_name", "cedula", "...")


class AlumnosTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    codigo = tables.Column(verbose_name='codigo')
    get_full_name = tables.Column(verbose_name='nombres', order_by =("apellido1"))    
    ver     = EnlaceColumn( accessor="codigo", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detAlumno/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="codigo", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updAlumno/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="codigo", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delAlumno/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = Alumno
        exclude = ('apellido1', 'apellido2', 'nombre1', 'nombre2', 'persona_ptr')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "codigo", "get_full_name", "cedula", "...", "ver", "editar", "borrar" )


class AlumnosTablePDF(tables.Table):
    get_full_name = tables.Column(verbose_name='nombres', order_by =("apellido1"))
    class Meta:
        model = Alumno
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("id", "get_full_name", "cedula", "...")

