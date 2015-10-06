# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0026_auto_20150923_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planpago',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='catedras.Materia', help_text=b'Solo Si Aplica / Si no dejar vacio', null=True, verbose_name=b'Materia'),
        ),
    ]
