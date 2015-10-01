# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0009_auto_20150902_1316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curso',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'curso', 'verbose_name_plural': 'cursos'},
        ),
        migrations.AlterField(
            model_name='curso',
            name='materias',
            field=models.ManyToManyField(help_text=b'Genera una linea de plan de pago por Examen Ordinario por cada alumno', to='catedras.Materia', through='catedras.CursoMateria'),
        ),
    ]
