# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0002_auto_20151030_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReciboDescuento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('porcentaje', models.DecimalField(verbose_name=b'Porcentaje', max_digits=3, decimal_places=0)),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=5, decimal_places=0)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'verbose_name': 'Recibo Descuento',
                'verbose_name_plural': 'Recibos Descuentos',
            },
        ),
    ]
