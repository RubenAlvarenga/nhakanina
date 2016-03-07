#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from .models import CursoAlumno
from apps.aranceles.models import Arancel
from .functions import ultimo_dia_del_mes, sumar_mes
from datetime import datetime, date
from django.contrib.auth.models import User




def esInscripto(sender, **kwargs): 
    from apps.finanzas.models import PlanPago
    p_curso_alumno = kwargs["instance"]
    monto_cuota = p_curso_alumno.curso.monto_cuota.monto
    cantidad_cuotas = p_curso_alumno.curso.cantidad_cuotas
    fecha = p_curso_alumno.curso.inicio
    #CUOTAS
    # if not PlanPago.objects.filter(curso_alumno=p_curso_alumno, concepto__in=Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=2) ):
    #     for cuota in range(cantidad_cuotas):
    #         ultimo_dia = ultimo_dia_del_mes(fecha)
    #         plan = PlanPago()
    #         plan.curso_alumno = p_curso_alumno
    #         plan.concepto = p_curso_alumno.curso.monto_cuota
    #         plan.total_cuotas = cantidad_cuotas
    #         plan.secuencia = cuota + 1 
    #         plan.vencimiento = ultimo_dia
    #         plan.monto = monto_cuota
    #         plan.created_by = User.objects.get(pk=2)
    #         plan.save()
    #         fecha = sumar_mes(ultimo_dia, 1)
    # else:
    for cuota in range(cantidad_cuotas):
        if not PlanPago.objects.filter(curso_alumno=p_curso_alumno, concepto__in=Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=2), total_cuotas=cantidad_cuotas, secuencia=cuota+1):
            ultimo_dia = ultimo_dia_del_mes(fecha)
            plan = PlanPago()
            plan.curso_alumno = p_curso_alumno
            plan.concepto = p_curso_alumno.curso.monto_cuota
            plan.total_cuotas = cantidad_cuotas
            plan.secuencia = cuota + 1
            plan.vencimiento = ultimo_dia
            plan.monto = monto_cuota
            plan.created_by = User.objects.get(pk=2)
            plan.save()
            fecha = sumar_mes(ultimo_dia, 1)
        else:
            ultimo_dia = ultimo_dia_del_mes(fecha)
            fecha = sumar_mes(ultimo_dia, 1)




    #MATRICULA
    if not PlanPago.objects.filter(curso_alumno=p_curso_alumno, concepto__in=Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=1) ):

        if p_curso_alumno.curso.fecha_tope_matriculacion and p_curso_alumno.curso.matricula_fpo:
            if p_curso_alumno.curso.fecha_tope_matriculacion < date.today():
                concepto = p_curso_alumno.curso.matricula_fpo
            else:
                concepto = p_curso_alumno.curso.matricula
        else: 
            concepto = p_curso_alumno.curso.matricula

        matricula = PlanPago()
        matricula.curso_alumno = p_curso_alumno
        matricula.concepto = concepto
        matricula.secuencia = 0 
        matricula.vencimiento = ultimo_dia_del_mes(p_curso_alumno.curso.inicio)
        matricula.monto = concepto.monto
        matricula.created_by = User.objects.get(pk=2)
        matricula.save()


   #EXAMENNES ORDINARIOS
    if p_curso_alumno.curso.materias.all() and p_curso_alumno.curso.examen_ordinario:
        for materia in p_curso_alumno.curso.materias.all():
            if not PlanPago.objects.filter(curso_alumno=p_curso_alumno, concepto__in=Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=3), materia=materia):
                plan_examen = PlanPago()
                plan_examen.curso_alumno = p_curso_alumno
                plan_examen.concepto = p_curso_alumno.curso.examen_ordinario
                plan_examen.secuencia = 0 
                #plan_examen.vencimiento = ultimo_dia_del_mes(p_curso_alumno.curso.inicio)
                plan_examen.monto = p_curso_alumno.curso.examen_ordinario.monto
                plan_examen.created_by = User.objects.get(pk=2)
                plan_examen.materia = materia
                plan_examen.save()

    # if not PlanPago.objects.filter(curso_alumno=p_curso_alumno, concepto__in=Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=3) ):
    #     if p_curso_alumno.curso.materias.all() and p_curso_alumno.curso.examen_ordinario:
    #         for materia in p_curso_alumno.curso.materias.all():
    #             plan_examen = PlanPago()
    #             plan_examen.curso_alumno = p_curso_alumno
    #             plan_examen.concepto = p_curso_alumno.curso.examen_ordinario
    #             plan_examen.secuencia = 0 
    #             #plan_examen.vencimiento = ultimo_dia_del_mes(p_curso_alumno.curso.inicio)
    #             plan_examen.monto = p_curso_alumno.curso.examen_ordinario.monto
    #             plan_examen.created_by = User.objects.get(pk=2)
    #             plan_examen.materia = materia
    #             plan_examen.save()
 


post_save.connect(esInscripto, sender=CursoAlumno)

