#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models.signals import m2m_changed, post_save, post_delete
from .models import ReciboPlanPago, PlanPago, Recibo
from apps.catedras.models import CursoMateria
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(m2m_changed, sender=ReciboPlanPago.plan_pago.through)
def pagaDesdeReciboPlanPago(sender, instance, **kwargs):
    planes = instance.plan_pago.all()
    for p in planes:
        p.estado = 'PAG'
        p.save()


@receiver(post_save, sender=ReciboPlanPago)
def ponePendientePlanPagoReciboAnulado(sender, instance, **kwargs):
    if instance.estado=='ANU':
        for plan in instance.plan_pago.all():
            instance.plan_pago.remove(plan.id)
            plan.estado='PEN'
            plan.save()
    else:
        pass


@receiver(post_save, sender=CursoMateria)
def agregaPlanPagoExamenOrdinarioPorAlumno(sender, instance, **kwargs):
    for alumno in instance.curso.get_alumnos.all():
        if not PlanPago.objects.filter(curso_alumno=alumno, concepto=instance.curso.examen_ordinario, materia=instance.materia):
            plan_pago = PlanPago()
            plan_pago.curso_alumno = alumno 
            plan_pago.materia = instance.materia
            plan_pago.concepto= instance.curso.examen_ordinario
            plan_pago.monto = instance.curso.examen_ordinario.monto
            plan_pago.created_by = User.objects.get(pk=2)
            plan_pago.save()

@receiver(post_delete, sender=CursoMateria)
def borraPlanPagoExamenOrdinarioPorAlumno(sender, instance, **kwargs):
    for alumno in instance.curso.get_alumnos.all():
        try: 
            aborrar = PlanPago.objects.get(curso_alumno=alumno, concepto=instance.curso.examen_ordinario, materia=instance.materia, estado='PEN')
            aborrar.delete()
        except:
            pass
