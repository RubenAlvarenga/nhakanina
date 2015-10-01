# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0002_auto_20150903_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumno',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Alumno', 'verbose_name_plural': 'Alumnos'},
        ),
    ]
