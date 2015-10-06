#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import get_object_or_404


class Persona(models.Model):
    cedula=models.CharField(max_length=10, verbose_name='Cédula', unique=True)
    nombre1=models.CharField(max_length=50, verbose_name='Nombre')
    nombre2=models.CharField(max_length=50, verbose_name='Segundo Nombre', blank=True)
    apellido1=models.CharField(max_length=50, verbose_name='Primer Apellido')
    apellido2=models.CharField(max_length=50, verbose_name='Segundo Apellido', blank=True)
    fecha_nacimiento=models.DateField(verbose_name='Nacimiento', blank=True, null=True)
    
    @property
    def get_full_name(self):
        if self.apellido2=='': return self.apellido1 +", "+ self.nombre1 +" "+ self.nombre2
        else: return self.apellido1 +" "+ self.apellido2 +', '+ self.nombre1 +" "+ self.nombre2

    @property
    def es_alumno(self):
        """IMPORTANTE debe ser id y no pk por ser un modelo heredado"""
        try: return Alumno.objects.get(id=self.id)
        except: return False
    
    class Meta:
        verbose_name = 'persona'
        verbose_name_plural = 'personas'
        ordering =[ 'apellido1', 'apellido2', 'nombre1']
        default_permissions = ('add', 'change', 'delete', 'view', 'list')

    def save(self, *args, **kwargs):
        cedula = getattr(self, 'cedula', False)
        if cedula: setattr(self, 'cedula', cedula.strip())
        nombre1 = getattr(self, 'nombre1', False)
        if nombre1: setattr(self, 'nombre1', nombre1.capitalize())
        nombre2 = getattr(self, 'nombre2', False)
        if nombre2: setattr(self, 'nombre2', nombre2.capitalize())
        apellido1 = getattr(self, 'apellido1', False)
        if apellido1: setattr(self, 'apellido1', apellido1.capitalize())
        apellido2 = getattr(self, 'apellido2', False)
        if apellido2: setattr(self, 'apellido2', apellido2.capitalize())        
        super(Persona, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s, %s (%s)' % (unicode(self.apellido1), unicode(self.nombre1), unicode(self.cedula))




class Alumno(Persona):
    codigo = models.AutoField(primary_key=True, verbose_name='Codigo Alumno')
    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    
    @property
    def get_cursos_activos(self):
        from apps.catedras.models import CursoAlumno
        cursos = CursoAlumno.objects.filter(alumno=self, estado='ACT')
        return cursos        
    
    def __unicode__(self):
        return '%s, %s' % (self.apellido1, self.nombre1)

    def save(self, *args, **kwargs):
        super(Alumno, self).save(*args, **kwargs)


