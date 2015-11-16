#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from apps.aranceles.models import TipoCarreraConcepto
from django.contrib.auth.models import User



class TimeStampModel(models.Model):
    created_by = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Descuento(TimeStampModel):
    #ejecuta la funcion corresponsiente que devuelve falso o verdadero
    CONDICIONES = (
        ('ninguno', 'Ninguno'), 
        ('es_socio_afemec', 'Socio de AFEMEC'), 
        ('es_docente_ise', 'Docente del ISE')
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')
    motivo = models.CharField(max_length=100, verbose_name='Motivo')
    tipo_carrera_concepto = models.ForeignKey(TipoCarreraConcepto, verbose_name='Tipo Carrera | Concepto', on_delete=models.PROTECT)
    cant_minima_concepto = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Cantidad Minima' )
    cant_maxima_concepto = models.DecimalField(max_digits=3, decimal_places=0, verbose_name='Cantidad Maxima' )
    porcentaje = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Porcentaje' )
    #funcion =  models.CharField(max_length=200,  verbose_name='Funcion a ejecutar', default='Ninguno')
    funcion = models.CharField(max_length=200, choices=CONDICIONES, default='ninguno', verbose_name='Condiciones')

    
    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __unicode__(self):
        return u'%s' % (unicode(self.motivo))








