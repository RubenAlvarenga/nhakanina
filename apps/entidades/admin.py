#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Persona, Alumno
from apps.finanzas.models import PlanPago


class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cedula', 'get_full_name')
    search_fields = ['cedula', 'apellido1', 'apellido2', 'nombre1', 'nombre2']
    list_display_links = ('get_full_name',)

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cedula', 'get_full_name')
    search_fields = ['cedula', 'apellido1', 'apellido2', 'nombre1', 'nombre2']
    list_display_links = ('get_full_name',)


class PlanPagoInine(admin.TabularInline):
    model = PlanPago
    readonly_fields = ('concepto', 'estado', 'vencimiento', 'secuencia', 'monto')
    template = 'catedras/planpago_inline.html'




admin.site.register(Persona, PersonaAdmin)
admin.site.register(Alumno, AlumnoAdmin)
