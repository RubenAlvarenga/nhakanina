# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0031_auto_20151102_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibodescuento',
            name='descuento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Descuento', to='descuentos.Descuento'),
        ),
    ]
