#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import PlanPago
import calendar
import datetime
from django.db import transaction
from django.template import Template, Context


def msg_render(msg):
    return Template(msg).render(Context())

def ultimo_dia_del_mes(fecha):
    firstweekday, days=calendar.monthrange(fecha.year, fecha.month)
    return datetime.date(fecha.year, fecha.month, days)

def sumar_mes(fecha, months):
    month = fecha.month - 1 + months
    year = fecha.year + month / 12
    month = month % 12 + 1
    day = min(fecha.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)


@transaction.atomic
def fracionar_plan(plan, cantidad, user):
    exito = False
    monto = plan.monto / cantidad
    try:
        with transaction.atomic():
            plan.monto = monto
            plan.total_cuotas = cantidad
            plan.secuencia = 1
            plan.save()
            fecha = sumar_mes(plan.vencimiento, 1)
            for i in range(1, cantidad):
                ultimo_dia = ultimo_dia_del_mes(fecha)
                plan_pago = PlanPago()
                plan_pago.curso_alumno = plan.curso_alumno
                plan_pago.concepto = plan.concepto
                plan_pago.secuencia = i+1
                plan_pago.vencimiento = ultimo_dia
                plan_pago.monto = monto 
                plan_pago.total_cuotas = cantidad
                plan_pago.created_by = user
                plan_pago.save()
                fecha = sumar_mes(ultimo_dia, 1)
            exito = True
    except:
        exito = False
        transaction.rollback()
    finally:
        return exito


def sumarTotalesPlanPago(planes):
    total=0
    for plan in planes:
        total = total + plan.monto
    return total

def restarDescuento(total, descuentos):
    total_con_descuento = total
    for d in descuentos:
        total_con_descuento = total_con_descuento - (total * d.porcentaje/100)
    return total_con_descuento