# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0007_auto_20150831_0020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curso',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'verbose_name': 'curso', 'verbose_name_plural': 'cursos'},
        ),
        migrations.AlterField(
            model_name='materia',
            name='nombre',
            field=models.CharField(unique=True, max_length=100, verbose_name=b'Nombre'),
        ),
    ]
