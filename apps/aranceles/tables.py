#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.conf import settings
from django_tables2  import  A
from django.utils.html import escape
from django.contrib.humanize.templatetags.humanize import intcomma

from .models import Concepto, Periodo, Arancel, TipoConcepto

ITEM_POR_PAGINA = 50

class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class ConceptosTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    fraccionable = tables.BooleanColumn(verbose_name='F/H')

    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detConcepto/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updConcepto/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delConcepto/", "icono":"glyphicon-remove" }, )

    class Meta:
        model = Concepto
        per_page=ITEM_POR_PAGINA
        exclude = ("funcion",)
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("selection", "...", "ver", "editar", "borrar"  )



class PeriodosTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detPeriodo/", "icono":"glyphicon-eye-open" }, )
    # editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updPeriodo/", "icono":"glyphicon-pencil" }, )
    # borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delPeriodo/", "icono":"glyphicon-remove" }, )

    class Meta:
        model = Periodo
        per_page=ITEM_POR_PAGINA
        exclude = ()
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("selection", "...", "ver")


class ArancelesTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )

    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detArancel/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updArancel/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delArancel/", "icono":"glyphicon-remove" }, )

    class Meta:
        model = Arancel
        per_page=ITEM_POR_PAGINA
        exclude = ('created', 'modified', 'created_by')
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("selection", "...", "ver", "editar", "borrar"  )


class TiposConceptosTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detArancel/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updArancel/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delArancel/", "icono":"glyphicon-remove" }, )

    class Meta:
        model = TipoConcepto
        per_page=ITEM_POR_PAGINA
        exclude = ()
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("selection", "...", "ver", "editar", "borrar"  )

