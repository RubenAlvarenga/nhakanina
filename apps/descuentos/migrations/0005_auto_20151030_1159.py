# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0004_delete_recibodescuento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descuento',
            name='estado',
        ),
        migrations.AddField(
            model_name='descuento',
            name='activo',
            field=models.BooleanField(default=True, verbose_name=b'Activo'),
        ),
    ]
