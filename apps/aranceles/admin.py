#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Periodo, TipoCarrera, TipoConcepto, TipoCarreraConcepto, Concepto, Arancel
from django.forms import TextInput
from django.db import models
from .forms import ConceptoForm

class TipoCarreraConceptoInline(admin.TabularInline):
    model = TipoCarreraConcepto
    extra = 1

class TipoCarreraAdmin(admin.ModelAdmin):
    inlines=[TipoCarreraConceptoInline]


admin.site.register(TipoConcepto)
admin.site.register(TipoCarrera, TipoCarreraAdmin)

class ConceptoInine(admin.TabularInline):
    model = Concepto
    form = ConceptoForm
    extra = 1

class TipoCarreraConceptoAdmin(admin.ModelAdmin):
    list_display=('id','tipo_carrera', 'tipo_concepto')
    list_display_links=('tipo_concepto',)
    list_filter = ('tipo_carrera', 'tipo_concepto',)
    inlines=[ConceptoInine]

class ConceptoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'max_length':'500'})},
    }
admin.site.register(TipoCarreraConcepto, TipoCarreraConceptoAdmin)
admin.site.register(Concepto, ConceptoAdmin,)

class ArancelInline(admin.TabularInline):
    model=Arancel
    extra=1

class PeriodoAdmin(admin.ModelAdmin):
    inlines=[ArancelInline]
    def save_model(self, request, obj, form, change): 
        obj.created_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change): 
        if formset.model == Arancel:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.created_by = request.user
                instance.save()
        else:
            formset.save()              

class ArancelAdmin(admin.ModelAdmin):
    list_display = ('id', 'monto', 'concepto')
    search_fields = ['concepto__concepto']
    list_display_links = ('concepto',)    

    def save_model(self, request, obj, form, change): 
        obj.created_by = request.user
        obj.save()


admin.site.register(Periodo, PeriodoAdmin,)
admin.site.register(Arancel, ArancelAdmin)
