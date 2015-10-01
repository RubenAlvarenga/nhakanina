# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cedula', models.CharField(unique=True, max_length=10, verbose_name=b'C\xc3\xa9dula')),
                ('nombre1', models.CharField(max_length=50, verbose_name=b'Nombre')),
                ('nombre2', models.CharField(max_length=50, verbose_name=b'Segundo Nombre', blank=True)),
                ('apellido1', models.CharField(max_length=50, verbose_name=b'Primer Apellido')),
                ('apellido2', models.CharField(max_length=50, verbose_name=b'Segundo Apellido', blank=True)),
                ('fecha_nacimiento', models.DateField(null=True, verbose_name=b'Fecha Nacimiento', blank=True)),
            ],
            options={
                'ordering': ['apellido1', 'apellido2', 'nombre1'],
                'verbose_name': 'persona',
                'verbose_name_plural': 'personas',
            },
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('persona_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='entidades.Persona')),
                ('codigo', models.AutoField(serialize=False, verbose_name=b'Codigo Alumno', primary_key=True)),
            ],
            options={
                'verbose_name': 'Alumno',
                'verbose_name_plural': 'Alumnos',
            },
            bases=('entidades.persona',),
        ),
    ]
