# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0005_auto_20150813_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpago',
            name='cantidad',
            field=models.DecimalField(default=1, verbose_name=b'Cantidad', max_digits=2, decimal_places=0),
        ),
        migrations.AddField(
            model_name='planpago',
            name='total_cuotas',
            field=models.DecimalField(default=1, verbose_name=b'Total Cuota', max_digits=2, decimal_places=0),
        ),
    ]
