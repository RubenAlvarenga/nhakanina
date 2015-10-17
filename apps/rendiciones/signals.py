#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models.signals import m2m_changed, post_save, post_delete, pre_delete
from .models import Rendicion
from apps.finanzas.models import Recibo
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(m2m_changed, sender=Rendicion.recibos.through)
def poneTotalenRendicion(sender, instance, **kwargs):
    total=0
    recibos = instance.recibos.all()
    for r in recibos:
        total=total+r.monto
    instance.total = total
    instance.save()

@receiver(pre_delete, sender=Rendicion)
def poneNoRendidoRecibos(sender, instance, **kwargs):
    recibos = instance.recibos.all()
    for r in recibos:
        r.rendido = False
        r.save()

@receiver(post_save, sender=Rendicion)
def poneRendidoRecibos(sender, instance, **kwargs):
    if instance.estado == 'APR':
        recibos = instance.recibos.all()
        for r in recibos:
            r.rendido = True
            r.save()


