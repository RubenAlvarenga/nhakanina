# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0010_auto_20150903_1556'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cursoalumno',
            options={'verbose_name': 'Matricula', 'verbose_name_plural': 'Matriculaciones'},
        ),
        migrations.AlterModelOptions(
            name='cursomateria',
            options={'verbose_name': 'Curso | Materia', 'verbose_name_plural': 'Cursos | Materias'},
        ),
    ]
