#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from apps.finanzas.models import Recibo
from django.contrib.auth.models import User


class TimeStampModel(models.Model):
    created_by = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True



class Rendicion(TimeStampModel):
    ESTADO = (
        ('PEN', 'Pendiente'),
        ('APR', 'Aprobado'),        
    )   
    nro_rendicion = models.DecimalField(max_digits=8, decimal_places=0, verbose_name='Nro Rendicion', unique=True )
    fecha_aprobacion = models.DateField(verbose_name='Aprobado el')
    aprobado_por = models.ForeignKey(User, editable=False, verbose_name='Aprobado por', related_name='aprobadopor_rendiciones', blank=True, null=True, on_delete=models.PROTECT)
    estado = models.CharField(max_length=3, choices=ESTADO, default='PEN', verbose_name='Estado')
    total = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Total' )
    recibos = models.ManyToManyField(Recibo, verbose_name='Recibos a rendir', help_text="Seleccione los recibos a rendir")

    class Meta:
        verbose_name = 'Rendicion'
        verbose_name_plural = 'Rendiciones'
        ordering = ('nro_rendicion', )
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    def __unicode__(self):
        return u'%s' '%s' % (self.nro_rendicion, self.estado)
