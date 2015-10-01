# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0012_auto_20150912_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='duracion',
            field=models.DecimalField(decimal_places=0, max_digits=2, blank=True, help_text=b'En meses', null=True, verbose_name=b'Duracion'),
        ),
    ]
