# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0029_auto_20151030_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibo',
            name='descuentos',
            field=models.ManyToManyField(to='descuentos.Descuento', null=True, through='finanzas.ReciboDescuento', blank=True),
        ),
        migrations.AlterField(
            model_name='recibodescuento',
            name='monto',
            field=models.DecimalField(null=True, verbose_name=b'Monto', max_digits=5, decimal_places=0, blank=True),
        ),
        migrations.AlterField(
            model_name='recibodescuento',
            name='porcentaje',
            field=models.DecimalField(null=True, verbose_name=b'Porcentaje', max_digits=3, decimal_places=0, blank=True),
        ),
    ]
