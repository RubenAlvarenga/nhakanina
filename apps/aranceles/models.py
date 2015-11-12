#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatewords


class TimeStampModel(models.Model):
    created_by = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

ESTADO = (
    ('ACT', 'Activo'), 
    ('HIS', 'Historico')
)
class Periodo(TimeStampModel):
    resolucion = models.CharField(max_length=8, unique=True, verbose_name='Resolucion')
    inicio = models.DateField(verbose_name='Inicio')
    fin = models.DateField(verbose_name='Fin', blank=True, null=True)
    estado = models.CharField(max_length=3, choices=ESTADO, default='ACT')
    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos de Aranceles'
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __unicode__(self):
        return u'%s [%s]' % (self.resolucion, self.estado)


class TipoCarrera(models.Model):
    titulo=models.CharField(max_length=255, verbose_name='Titulo')
    class Meta:
        verbose_name = 'Tipo Carrera'
        verbose_name_plural = 'Tipos de Carreras'
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __unicode__(self):
        return u'%s' % (self.titulo)

class TipoConcepto(models.Model):
    titulo=models.CharField(max_length=255, verbose_name='Titulo')
    class Meta:
        verbose_name = 'TipoConcepto'
        verbose_name_plural = 'Tipos de Conceptos'
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __unicode__(self):
        return u'%s' % (self.titulo)

class TipoCarreraConcepto(models.Model):
    tipo_carrera = models.ForeignKey(TipoCarrera, verbose_name='Tipo Carrera', on_delete=models.PROTECT)    
    tipo_concepto = models.ForeignKey(TipoConcepto, verbose_name='Tipo Concepto', on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Carrera | Concepto'
        verbose_name_plural = 'Carreras | Conceptos'
        unique_together = (('tipo_carrera', 'tipo_concepto' ),)
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __unicode__(self):
        return u'%s| %s' % (unicode(self.tipo_carrera)[0:3], truncatewords(self.tipo_concepto, 1))


class Concepto(models.Model):
    tipo_concepto = models.ForeignKey(TipoCarreraConcepto, verbose_name='Tipo Concepto', on_delete=models.PROTECT)
    concepto=models.CharField(max_length=255, verbose_name='Titulo')
    estado = models.BooleanField(default=True, verbose_name='Activo')
    fraccionable = models.BooleanField(default=False, verbose_name='Fraccionable')
    fraccionable_hasta=models.DecimalField(max_digits=2, decimal_places=0, verbose_name='hasta', blank=True, null=True )    
    funcion = models.CharField(max_length=255, verbose_name='Funcion',  help_text="Funcion especial para calculos de cobro", blank=True, null=True)
    class Meta:
        verbose_name = 'Concepto'
        verbose_name_plural = 'Conceptos'
        unique_together = (('tipo_concepto', 'concepto' ),)
        ordering = ['tipo_concepto', 'id']
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __unicode__(self):
        return u'[%s] %s' % (self.tipo_concepto, self.concepto)

class Arancel(TimeStampModel):
    resolucion = models.ForeignKey(Periodo, verbose_name='Resolucion', on_delete=models.PROTECT)
    concepto = models.ForeignKey(Concepto, verbose_name='Concepto', on_delete=models.PROTECT)
    monto=models.DecimalField(max_digits=8, decimal_places=0, verbose_name='Monto', blank=False )
    activo = models.BooleanField(default=True, verbose_name='Activo')
    class Meta:
        verbose_name = 'Arancel'
        verbose_name_plural = 'Aranceles'
        unique_together = (('resolucion', 'concepto' ),)
        ordering = ['concepto',]
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __unicode__(self):
        return u'%s (%s)' % (self.concepto, str(self.monto))





