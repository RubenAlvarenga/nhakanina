#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from .models import Descuento
from django.utils.safestring import mark_safe
from django.conf import settings
from  django_tables2  import  A
from django.utils.html import escape
ITEM_POR_PAGINA = 50

class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class DescuentoTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )    
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detDescuento/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updDescuento/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delDescuento/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = Descuento
        exclude = ('created', 'modified')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("selection", "id", "...", "ver", "editar", "borrar" )

class DescuentoTablePDF(tables.Table):
    class Meta:
        model = Descuento
        exclude = ('created', 'modified')
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("id", "..." )

