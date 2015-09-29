#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import PlanPago, Recibo, ReciboPlanPago
from apps.catedras.models import CursoAlumno
from apps.aranceles.models import Arancel
from .forms import PlanPagoForm, ReciboPlanPagoForm, ReciboForm



class PlanPagoAdmin(admin.ModelAdmin):
    #raw_id_fields = ('curso_alumno',) 
    form = PlanPagoForm
    def save_model(self, request, obj, form, change):
        obj.monto = obj.concepto.monto
        try:obj.secuencia=PlanPago.objects.filter(curso_alumno=obj.curso_alumno, concepto=obj.concepto).values('secuencia').order_by('-secuencia')[0]['secuencia'] + 1
        except: pass

        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Excluir Aranceles de Matricula y Cuota y varios
        if db_field.name == "concepto":
            kwargs["queryset"] = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto__in = [3,4])
        return super(PlanPagoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



class ReciboAdmin(admin.ModelAdmin):
    form = ReciboForm
    def save_model(self, request, obj, form, change):
        obj.monto = obj.concepto.monto * obj.cantidad
        obj.cajero = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Excluir Aranceles de Matricula y Cuota
        if db_field.name == "concepto":
            kwargs["queryset"] = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto__in = [5])
        return super(ReciboAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



class ReciboPlanPagoAdmin(admin.ModelAdmin):
    """
        Calcula cantidad de concepto, el concepto, calculo el monto
        obtiene el cajero
        envia signals a plan de pago para cambiar a pagado
    """
    form = ReciboPlanPagoForm
    filter_horizontal = ('plan_pago',)
    def save_model(self, request, obj, form, change):
        planes = PlanPago.objects.filter(pk__in=request.POST.getlist('plan_pago'))
        total=0
        concepto=[]
        for p in planes:
            total=total+p.monto
            concepto.append(p.concepto)
        if len(set(concepto)) == 1:
            obj.concepto = set(concepto).pop()
        obj.monto = total
        obj.cantidad = len(planes)
        obj.cajero = request.user
        obj.save()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Excluir Aranceles de Matricula y Cuota
        if db_field.name == "plan_pago":
            kwargs["queryset"] = PlanPago.objects.filter(estado='PEN')
        return super(ReciboPlanPagoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(PlanPago, PlanPagoAdmin)
admin.site.register(Recibo, ReciboAdmin)
admin.site.register(ReciboPlanPago, ReciboPlanPagoAdmin)



