#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.conf import settings
from django_tables2  import  A
from django.utils.html import escape
from django.contrib.humanize.templatetags.humanize import intcomma

from .models import Rendicion
from apps.finanzas.models import Recibo

ITEM_POR_PAGINA = 50

class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class RendicionesTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )

    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detRendicion/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updRendicion/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delRendicion/", "icono":"glyphicon-remove" }, )

    class Meta:
        model = Rendicion
        per_page=ITEM_POR_PAGINA
        exclude = ()
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("selection", "...", "ver", "editar", "borrar"  )



class RecibosTable(tables.Table):
    #selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )    
    get_recibo = tables.LinkColumn('finanzas:det_recibo', args=[A('pk')], verbose_name='Recibo', order_by=("serie", "nro_recibo"), attrs={'style':"font-weight:bold"})
    cantidad = tables.Column(verbose_name='Can')
    get_concepto_planpago = tables.Column(verbose_name='Concepto', orderable=False)
    monto = tables.Column(attrs={"td": {"class": "campo-align-right"}})
    #ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detRecibo/", "icono":"glyphicon-eye-open" }, )
    def render_monto(self, value):
        return intcomma(value)
    class Meta:
        model = Recibo
        exclude = ('created', 'modified', 'cajero', 'motivo_anulacion', 'fecha_anulacion', 'usuario_anulacion', 'serie', 'nro_recibo', 'rendido', 'persona', 'concepto')
        per_page=1000
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("id", "get_recibo",  "fecha",  "...", "monto")


class RecibosTablePDF(tables.Table):
    get_concepto_planpago = tables.Column(verbose_name='Concepto')
    class Meta:
        model = Recibo
        exclude = ('created', 'modified', 'cajero', 'motivo_anulacion', 'fecha_anulacion', 'usuario_anulacion', 'rendido', 'concepto')


class RecibosTableCSV(tables.Table):
    get_concepto_planpago_declaracion = tables.Column(verbose_name='Concepto')
    deposito_comprobante = tables.Column(verbose_name='Comprobante de Depósito Nro')
    deposito_fecha = tables.Column(verbose_name='Fecha de Depósito')
    deposito_monto = tables.Column(verbose_name='Monto del Depósito')
    class Meta:
        model = Recibo
        fields = ('get_concepto_planpago_declaracion', 'nro_recibo', 'serie', 'fecha', 'monto', 'deposito_comprobante', 'deposito_fecha', 'deposito_monto')

