# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0006_auto_20150830_1946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cursomateria',
            options={'verbose_name': 'Curso/Materia', 'verbose_name_plural': 'Cursos/Materias'},
        ),
    ]
