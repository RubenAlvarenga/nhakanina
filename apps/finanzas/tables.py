#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from apps.entidades.models import Alumno, Persona
from .models import PlanPago, Recibo
from django.utils.safestring import mark_safe
from django.conf import settings
from django_tables2  import  A
from django.utils.html import escape
from django.contrib.humanize.templatetags.humanize import intcomma
ITEM_POR_PAGINA = 50

class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class CobrarColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><button type="button" class="btn btn-info btn-xs"><span class="glyphicon '+str(self.attrs["icono"])+'"></span> '+str(self.attrs["texto"])+'</button></a>')


class AlumnosTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    get_full_name = tables.Column(verbose_name='nombres', order_by =("apellido1"))    
    ver     = EnlaceColumn( accessor="codigo", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detAlumno/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="codigo", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updAlumno/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="codigo", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delAlumno/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = Alumno
        exclude = ('apellido1', 'apellido2', 'nombre1', 'nombre2', 'persona')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "codigo" , "get_full_name", "cedula", "...", "ver", "editar", "borrar" )



class PersonasTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    get_full_name = tables.LinkColumn('finanzas:det_persona', args=[A('pk')], verbose_name='nombres', order_by =("apellido1", "apellido2"), attrs={'style':"font-weight:bold"})    
    cobrar     = CobrarColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detPersona/", "icono":"glyphicon-download-alt", "texto":"cobrar" }, )
    class Meta:
        model = Persona
        exclude = ('apellido1', 'apellido2', 'nombre1', 'nombre2', 'persona')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "get_full_name", "cedula", "...", "cobrar")


class PlanPagoTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    vencimiento = tables.DateColumn(verbose_name='Vencimiento')
    cantidad = tables.Column(verbose_name='Cant')
    concepto = tables.Column(accessor='concepto.concepto')
    alumno = tables.Column(accessor='curso_alumno.alumno')
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detPlanPago/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updPlanPago/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delPlanPago/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = PlanPago
        exclude = ('created', 'modified', 'curso_alumno', 'observaciones', 'created_by', 'authorized_by', 'total_cuotas', 'secuencia', 'estado')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("selection", "id", "alumno",  "...", )

class PlanPagoAplReciboTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    vencimiento = tables.Column(verbose_name='Vencimiento')
    class Meta:
        model = PlanPago
        exclude = ('created', 'modified', 'curso_alumno', 'observaciones', 'created_by', 'authorized_by', 'total_cuotas', 'secuencia')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id","...", )


class RecibosTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    
    get_recibo = tables.LinkColumn('finanzas:det_recibo', args=[A('pk')], verbose_name='Recibo', order_by=("serie", "nro_recibo"), attrs={'style':"font-weight:bold"})
    cantidad = tables.Column(verbose_name='Can')
    #rendido = tables.Column(verbose_name='Ren')
    get_concepto_planpago = tables.Column(verbose_name='Concepto', orderable=False)
    monto = tables.Column(attrs={"td": {"class": "campo-align-right"}})
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detRecibo/", "icono":"glyphicon-eye-open" }, )
    def render_monto(self, value):
        return intcomma(value)
    class Meta:
        model = Recibo
        exclude = ('created', 'modified', 'cajero', 'motivo_anulacion', 'fecha_anulacion', 'usuario_anulacion', 'serie', 'nro_recibo', 'rendido', 'persona', 'concepto')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover table-small" }
        sequence = ("selection", "id", "get_recibo",  "fecha",  "...", "monto", "ver" )



class RecibosTablePDF(tables.Table):
    get_concepto_planpago = tables.Column(verbose_name='Concepto')
    class Meta:
        model = Recibo
        exclude = ('created', 'modified', 'cajero', 'motivo_anulacion', 'fecha_anulacion', 'usuario_anulacion', 'rendido', 'concepto')
        per_page=ITEM_POR_PAGINA
