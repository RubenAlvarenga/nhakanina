# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rendiciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rendicion',
            name='fecha_aprobacion',
            field=models.DateField(null=True, verbose_name=b'Aprobado el', blank=True),
        ),
        migrations.AlterField(
            model_name='rendicion',
            name='total',
            field=models.DecimalField(null=True, verbose_name=b'Total', max_digits=10, decimal_places=0, blank=True),
        ),
    ]
