#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from apps.aranceles.models import Concepto, TipoCarrera, Arancel
from apps.entidades.models import Alumno
from django.contrib.auth.models import User


class TimeStampModel(models.Model):
    created_by = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Grupo(models.Model):
    grupo = models.CharField(max_length=100, verbose_name='Grupo')
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
    def __unicode__(self):
        return u'%s' % (self.grupo)

class Carrera(models.Model):
    tipo = models.ForeignKey(TipoCarrera, verbose_name='Tipo Carrera', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    grupo = models.ForeignKey(Grupo, verbose_name='Grupo', blank=True, null=True, on_delete=models.PROTECT)
    duracion = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Duracion', help_text="En meses", blank=True, null=True )
    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering = ('tipo', 'grupo', 'nombre')
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    def __unicode__(self):
        return u'%s %s %s' % (str(self.tipo)[0:3], self.grupo, self.nombre)

class Materia(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    def __unicode__(self):
        return u'%s' % (self.nombre)

class Semana(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    class Meta:
        verbose_name = 'Semana'
        verbose_name_plural = 'Semanas'
    def __unicode__(self):
        return u'%s' % (self.nombre)

from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
class Curso(models.Model):
    carrera = models.ForeignKey(Carrera, verbose_name='Carrera', on_delete=models.PROTECT)
    inicio = models.DateField(verbose_name='Inicio')
    fin = models.DateField(verbose_name='Fin', blank=True, null=True)
    dias = models.ManyToManyField(Semana, verbose_name='Dias de Clase',)
    turno = models.CharField(max_length=100, verbose_name='Turno - Seccion')

    matricula = models.ForeignKey(Arancel, verbose_name='Matricula Normal', help_text='Periodo Ordinario de Matriculacion', on_delete=models.PROTECT)
    matricula_fpo = models.ForeignKey(Arancel, verbose_name='Matricula FPO', related_name='arancel_matricula_fpo', help_text='Fuera del Periodo Ordinario de Matriculacion [*Si Aplica]', blank=True, null=True, on_delete=models.PROTECT)
    fecha_tope_matriculacion = models.DateField(verbose_name='Fecha tope de Matriculacion', blank=True, null=True, help_text='Para calcular el monto de la Matricula [*Si Aplica]')
    monto_cuota = models.ForeignKey(Arancel, verbose_name='Monto Cuota', related_name='arancel_monto_cuota', on_delete=models.PROTECT)
    cantidad_cuotas = models.DecimalField(max_digits=2, decimal_places=0, verbose_name='Cantidad de Cuotas', help_text='Importante para generar plan de pagos')
    
    materias = models.ManyToManyField(Materia, help_text='Genera una linea de plan de pago por Examen Ordinario por cada alumno', through='CursoMateria')
    examen_ordinario = models.ForeignKey(Arancel, verbose_name='Monto Examen Ordinario', related_name='arancel_examen_ordinario', on_delete=models.PROTECT)
    examen_extra = models.ManyToManyField(Arancel, verbose_name='Otros Examenes', related_name='arancel_examen_extra')
    

    aranceles = models.ManyToManyField(Arancel, verbose_name='Aranceles Aplicables', related_name='arancel_aranceles')
    estado = models.BooleanField(default=True, verbose_name='Habilitado')

    class Meta:        
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    def __unicode__(self):
        return u'%s(%s) %s' % (self.carrera, str(self.inicio.year), unicode(self.turno))

    @property
    def get_alumnos(self):
        return CursoAlumno.objects.filter(curso=self)



    
    # @property
    # def get_aranceles_extra(self):
    #     aranceles_extra = self.aranceles.exclude(concepto__tipo_concepto__tipo_concepto__in=[5], resolucion__estado='HIS')
    #     return aranceles_extra

    def clean(self):
        try:
            if self.matricula.concepto.tipo_concepto.tipo_carrera.id != self.carrera.tipo.id:
                raise ValidationError({'matricula': u'La matricula no se corresponde con el Tipo de Carrera Seleccionado: '+unicode(self.carrera.tipo.titulo)})
            if self.matricula_fpo:
                if self.matricula_fpo.concepto.tipo_concepto.tipo_carrera.id != self.carrera.tipo.id:
                    raise ValidationError({'matricula_fpo': u'La matricula FPO no se corresponde con el Tipo de Carrera Seleccionado: '+unicode(self.carrera.tipo.titulo)})            
                if not self.fecha_tope_matriculacion:
                    raise ValidationError({'fecha_tope_matriculacion': u'Ingrese la fecha de vigencia de la Matricula Fuera del Periodo Ordinario '})
            if self.monto_cuota.concepto.tipo_concepto.tipo_carrera.id != self.carrera.tipo.id:
                raise ValidationError({'monto_cuota': u'La cuota no se corresponde con el Tipo de Carrera Seleccionado: '+unicode(self.carrera.tipo.titulo)})
            # for Arancel in self.aranceles.all():
            #     if Arancel.concepto.tipo_concepto.tipo_carrera.id != self.carrera.tipo.id:
            #         raise ValidationError({'aranceles': u'Aranceles no se corresponden con el Tipo de carrera Seleccionado'})
        except ObjectDoesNotExist: pass

class CursoMateria(models.Model):
    curso = models.ForeignKey(Curso, verbose_name='Curso')
    materia = models.ForeignKey(Materia, verbose_name='Materia', on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Curso | Materia'
        verbose_name_plural = 'Cursos | Materias'
        unique_together = (('curso', 'materia'),)
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    def __unicode__(self):
        return u'%s - %s' % (self.curso, self.materia)

class CursoAlumno(TimeStampModel):
    ESTADO = (
        ('ACT', 'Activo'), 
        ('HIS', 'Historico')
    )
    curso = models.ForeignKey(Curso, verbose_name='Carrera - Curso', on_delete=models.PROTECT)
    alumno = models.ForeignKey(Alumno, verbose_name='Alumno', on_delete=models.PROTECT)
    fecha_inscripcion = models.DateField(verbose_name='Fecha de Inscripción')
    estado = models.CharField(max_length=3, choices=ESTADO, default='ACT', verbose_name='Estado')
    observacion = models.TextField( verbose_name='Observaciones', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Matricula'
        verbose_name_plural = 'Matriculaciones'
        unique_together = (('curso', 'alumno'),)
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    
    @property
    def get_planPago(self):
        from apps.finanzas.models import PlanPago
        plan = PlanPago.objects.filter(curso_alumno=self).order_by('concepto', 'secuencia')
        return plan
    @property
    def get_pendientes(self):
        from apps.finanzas.models import PlanPago
        plan = PlanPago.objects.filter(curso_alumno=self, estado='PEN').order_by('concepto', 'secuencia')
        return plan    


    def __unicode__(self):
        return u"%s (%s) [%s]" % (self.alumno, self.alumno.cedula, self.curso)








