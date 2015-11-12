# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0004_delete_recibodescuento'),
        ('finanzas', '0028_auto_20151028_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReciboDescuento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('porcentaje', models.DecimalField(verbose_name=b'Porcentaje', max_digits=3, decimal_places=0)),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=5, decimal_places=0)),
                ('descuento', models.ForeignKey(verbose_name=b'Descuento', to='descuentos.Descuento')),
                ('recibo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Recibo', to='finanzas.Recibo')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'verbose_name': 'Recibo Descuento',
                'verbose_name_plural': 'Recibos Descuentos',
            },
        ),
        migrations.AddField(
            model_name='recibo',
            name='descuentos',
            field=models.ManyToManyField(to='descuentos.Descuento', through='finanzas.ReciboDescuento'),
        ),
    ]
