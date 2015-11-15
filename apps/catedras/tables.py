#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from .models import Curso, CursoAlumno, Carrera, Materia
from django.utils.safestring import mark_safe
from django.conf import settings
from django_tables2  import  A
from django.utils.html import escape
from django.contrib.humanize.templatetags.humanize import intcomma
ITEM_POR_PAGINA = 50

class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')


class CursosTable(tables.Table):
    anho = tables.Column(accessor='inicio.year', verbose_name='Año', order_by=("inicio"))
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detCurso/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updCurso/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delCurso/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = Curso
        exclude = ('inicio', 'fin', 'matricula', 'matricula_fpo', 'fecha_tope_matriculacion', 'monto_cuota', 'cantidad_cuotas', 'examen_ordinario')
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "anho", "id", "...", "ver", "editar", "borrar" )



class CursosTablePDF(tables.Table):
    anho = tables.Column(accessor='inicio.year', verbose_name='Año', order_by=("inicio"))
    class Meta:
        model = Curso
        exclude = ()





class CarrerasTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detCarrera/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updCarrera/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delCarrera/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = Carrera
        exclude = ()
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "...", "ver", "editar", "borrar")



class CarrerasTablePDF(tables.Table):
    anho = tables.Column(accessor='inicio.year', verbose_name='Año', order_by=("inicio"))
    class Meta:
        model = Carrera
        exclude = ()


class MateriasTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detMateria/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updMateria/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delMateria/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = Materia
        exclude = ()
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "...", "ver", "editar", "borrar")


class MateriasTablePDF(tables.Table):
    class Meta:
        model = Materia
        exclude = ()
        per_page=ITEM_POR_PAGINA



class CursoAlumnoTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detCursoAlumno/", "icono":"glyphicon-eye-open" }, )
    #editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updCurso/", "icono":"glyphicon-pencil" }, )
    #borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delCurso/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = CursoAlumno
        exclude = ['created_by', 'created', 'modified', 'observacion']
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "...", "ver")
