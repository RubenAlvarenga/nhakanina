# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0003_auto_20150811_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallereciboplan',
            name='plan_pago',
        ),
        migrations.RemoveField(
            model_name='detallereciboplan',
            name='recibo',
        ),
        migrations.AlterField(
            model_name='reciboplanpago',
            name='plan_pago',
            field=models.ManyToManyField(to='finanzas.PlanPago'),
        ),
        migrations.DeleteModel(
            name='DetalleReciboPlan',
        ),
    ]
