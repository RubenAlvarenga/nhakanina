#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from apps.aranceles.models import Arancel
from apps.entidades.models import Alumno, Persona
from django.contrib.auth.models import User
from apps.catedras.models import CursoAlumno, CursoMateria, Materia
from apps.descuentos.models import Descuento
from datetime import date, datetime
from apps.functions import mesificar

class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True



class Recibo(TimeStampModel):
    ESTADO = (
        ('PRO', 'Procesado'),
        ('ANU', 'Anulado'),
    )
    fecha = models.DateField(verbose_name='Fecha')
    nro_recibo = models.DecimalField(max_digits=8, decimal_places=0, verbose_name='Nro Recibo' )
    serie =  models.CharField(max_length=1, default='I', verbose_name='Serie')
    estado = models.CharField(max_length=3, choices=ESTADO, default='PRO', verbose_name='Estado')
    persona = models.ForeignKey(Persona, verbose_name='Persona/Alumno', on_delete=models.PROTECT)
    cajero = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=3, decimal_places=0, verbose_name='Cantidad' )
    monto = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Monto' )
    rendido = models.BooleanField(default=False, verbose_name='Rendido', editable=False)
    concepto = models.ForeignKey(Arancel, verbose_name='Concepto', on_delete=models.PROTECT)
    motivo_anulacion = models.TextField( verbose_name='Motivo Anulacion', blank=True, null=True)
    fecha_anulacion = models.DateTimeField(blank=True, null=True, editable=False)
    usuario_anulacion = models.ForeignKey(User, editable=False, related_name='usuario_anulacion_recibo', blank=True, null=True, on_delete=models.PROTECT)

    descuentos = models.ManyToManyField(Descuento, through='ReciboDescuento', blank=True)


    @property
    def get_recibo(self):
        return u'%s-%s' % (self.serie, self.nro_recibo)

    @property
    def get_rendido(self):
        from apps.rendiciones.models import Rendicion
        if Rendicion.objects.filter(recibos=self): return True
        else: return False

    @property
    def get_concepto_planpago(self):
        concepto = unicode(self.concepto.concepto.tipo_concepto.tipo_carrera.titulo[:3] +'|'+ unicode(self.concepto.concepto.tipo_concepto.tipo_concepto)) +' '+unicode(self.concepto.concepto.concepto)
        extra=''
        if self.estado=='ANU':
            concepto = '[ANULADO] ' + concepto
        try:
            if ReciboPlanPago.objects.get(pk=self.id).plan_pago.all():
                for recibo in ReciboPlanPago.objects.get(pk=self.id).plan_pago.all():
                    if recibo.materia:
                        extra = extra +', '+ recibo.materia.nombre 
            if self.concepto.concepto.tipo_concepto.tipo_concepto.id == 2:
                for plan in ReciboPlanPago.objects.get(pk=self.id).plan_pago.all():
                    extra = extra +', '+ mesificar(plan.vencimiento.month)
            if extra:
                concepto = concepto + " ("+(unicode(extra.strip(", ")))+")"
        except: pass
        return concepto

    @property
    def get_estado(self):
        from apps.rendiciones.models import Rendicion
        try: return Rendicion.objects.filter(recibos=self.id)
        except: return False


    @property
    def get_planes(self):
        """ IMPORTTANTE PARA LA ANULACION NO HACER CAMBIOS"""
        try: return ReciboPlanPago.objects.get(pk=self.id)
        except: return False

    class Meta:
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'
        unique_together = (('nro_recibo', 'serie'),)
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        
    def __unicode__(self):
        return u'%s-%s (%s)' % (self.serie, self.nro_recibo, self.monto)

from django.core.exceptions import ValidationError, ObjectDoesNotExist
class PlanPago(TimeStampModel):
    ESTADO = (
        ('PEN', 'Pendiente'), 
        ('PAG', 'Pagado'),
        ('ANU', 'Anulado'),
        ('EXO', 'Exonerado'),
    )
    curso_alumno = models.ForeignKey(CursoAlumno, verbose_name='Curso | Alumno', on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Cantidad', default=1)
    concepto = models.ForeignKey(Arancel, verbose_name = 'Concepto', on_delete=models.PROTECT)
    total_cuotas = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Total Cuota', default=1 )
    secuencia = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Secuencia', default=0 )
    vencimiento = models.DateField(verbose_name='Fecha de Vencimiento', blank=True, null=True )
    estado = models.CharField(max_length=3, choices=ESTADO, default='PEN', verbose_name='Estado')
    monto = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Monto' )

    materia = models.ForeignKey(Materia, verbose_name='Materia', blank=True, null=True, on_delete=models.PROTECT, help_text='Solo Si Aplica / Si no dejar vacio')

    created_by = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    authorized_by = models.ForeignKey(User, editable=False, verbose_name='Autorizado por', related_name='authorized_finanzas', blank=True, null=True, on_delete=models.PROTECT)
    observaciones = models.TextField( verbose_name='Observaciones', blank=True, null=True)

    class Meta:
        verbose_name = 'Plan de Pago'
        verbose_name_plural = 'Planes'
        unique_together = (('curso_alumno', 'concepto', 'secuencia', 'materia'), )
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
        ordering = ['-estado', '-id']

    @property
    def get_vencido(self):
        if date.today() > self.vencimiento:return True
        else: return False
    @property
    def get_recibo(self):
        try: return ReciboPlanPago.objects.get(plan_pago = self)
        except: return None
    @property
    def get_concepto_abreviado(self):
        if self.concepto.concepto.tipo_concepto.tipo_concepto.id==2 or self.concepto.concepto.tipo_concepto.tipo_concepto.id==1:
            concepto_abreviado = "%s %s" % (unicode(self.concepto.concepto.tipo_concepto.tipo_concepto.titulo), unicode(self.concepto.concepto.concepto) )
        else:
            concepto_abreviado = "%s" % (unicode(self.concepto.concepto.concepto) )
        if self.materia:
            concepto_abreviado = concepto_abreviado +" ("+ unicode(self.materia.nombre)+")"
        return concepto_abreviado

    @property
    def get_cuotasecuencia(self):
        if self.secuencia: return "%s/%s" % (unicode(self.secuencia), unicode(self.total_cuotas))
        else: return ""


    def clean(self):
        try:
            if self.materia and self.curso_alumno:
                if self.materia not in self.curso_alumno.curso.materias.all():
                    raise ValidationError({'materia': u'La materia seleccionada no figura como materia del curso: '+unicode(self.curso_alumno.curso)})
        except ObjectDoesNotExist: pass
        try:
            if self.concepto.concepto.tipo_concepto.tipo_carrera.id != self.curso_alumno.curso.carrera.tipo.id:
                raise ValidationError({'concepto': u'El concepto seleccionado no se corresponde al tipo de carrera del curso: '+unicode(self.curso_alumno.curso.carrera.tipo)})
        except ObjectDoesNotExist: pass

    def __unicode__(self):
        return u'%s' % (self.concepto.concepto)


    

class ReciboPlanPago(Recibo):
    plan_pago = models.ManyToManyField(PlanPago)
    def save(self, *args, **kwargs):
        super(ReciboPlanPago, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'Recibo aplicado a Plan'
        verbose_name_plural = 'Recibos aplicados a Planes'



class ReciboDescuento(models.Model):
    recibo = models.ForeignKey(Recibo, verbose_name='Recibo', on_delete=models.PROTECT)
    descuento = models.ForeignKey(Descuento, verbose_name='Descuento', on_delete=models.PROTECT)

    porcentaje = models.DecimalField(max_digits=3, decimal_places=0, verbose_name='Porcentaje', null=True, blank=True )
    monto = models.DecimalField(max_digits=7, decimal_places=0, verbose_name='Monto', null=True, blank=True )

    class Meta:
        verbose_name = 'Recibo Descuento'
        verbose_name_plural = 'Recibos Descuentos'
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def __unicode__(self):
        return u'%s %s' % (unicode(self.porcentaje), unicode(self.monto))