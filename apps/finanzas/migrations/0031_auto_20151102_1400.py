# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0030_auto_20151102_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibo',
            name='descuentos',
            field=models.ManyToManyField(to='descuentos.Descuento', through='finanzas.ReciboDescuento', blank=True),
        ),
        migrations.AlterField(
            model_name='recibodescuento',
            name='monto',
            field=models.DecimalField(null=True, verbose_name=b'Monto', max_digits=7, decimal_places=0, blank=True),
        ),
    ]
