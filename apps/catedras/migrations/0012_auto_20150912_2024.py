# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0011_auto_20150910_0043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carrera',
            options={'ordering': ('tipo', 'grupo', 'nombre'), 'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Carrera', 'verbose_name_plural': 'Carreras'},
        ),
        migrations.AlterModelOptions(
            name='cursoalumno',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Matricula', 'verbose_name_plural': 'Matriculaciones'},
        ),
        migrations.AlterModelOptions(
            name='cursomateria',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Curso | Materia', 'verbose_name_plural': 'Cursos | Materias'},
        ),
        migrations.AlterModelOptions(
            name='materia',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Materia', 'verbose_name_plural': 'Materias'},
        ),
    ]
