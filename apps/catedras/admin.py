# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Grupo, Carrera, Curso, CursoAlumno, Materia, CursoMateria, Semana
from apps.aranceles.models import Arancel
from apps.finanzas.models import PlanPago
from .forms import CursoForm

class CarreraAdmin(admin.ModelAdmin):
    list_display=('id', 'tipo', 'grupo', 'nombre', 'duracion' )

class CursoMateriaInline(admin.TabularInline):
    model = CursoMateria
    extra = 1

class PlanPagoInine(admin.TabularInline):
    model = PlanPago
    extra = 0
    readonly_fields = ('concepto', 'estado', 'vencimiento', 'secuencia', 'monto')
    template = 'admin/catedras/planpago_inline.html'

class CursoAdmin(admin.ModelAdmin):
    form = CursoForm
    filter_horizontal = ('aranceles', 'examen_extra')
    list_display=('id', 'carrera', 'turno', 'get_anho' )
    inlines = (CursoMateriaInline, )
    search_fields = ['carrera__nombre', 'turno', 'inicio']
    list_display_links = ('turno',)

    def get_anho(self, obj):
        return obj.inicio.year

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtrar Aranceles de Matricula
        if db_field.name == "matricula" or db_field.name == "matricula_fpo":
            kwargs["queryset"] = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=1)
        # Filtrar Aranceles de Cuota
        if db_field.name == "monto_cuota":
            kwargs["queryset"] = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=2)
        # Filtrar Aranceles de Cuota
        if db_field.name == "examen_ordinario":
            kwargs["queryset"] = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=3)
        return super(CursoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "examen_extra":
            kwargs["queryset"] = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=3) #evaluacion
        return super(CursoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == "aranceles":
            kwargs["queryset"] = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto__in=[4,5]) #evaluacion, bienes, alquileres
        return super(CursoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class MateriaAdmin(admin.ModelAdmin):
    inlines = (CursoMateriaInline, ) 

class CursoAlumnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'get_cedula', 'curso')
    search_fields = ['alumno__cedula']
    list_display_links = ('alumno',)
    inlines=[PlanPagoInine]
    raw_id_fields=('curso', 'alumno')
    def save_model(self, request, obj, form, change): 
        obj.created_by = request.user
        obj.save()
    def get_cedula(self, obj):
        return obj.alumno.cedula





admin.site.register(Grupo)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(CursoAlumno, CursoAlumnoAdmin)
admin.site.register(CursoMateria)




