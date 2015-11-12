# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0006_auto_20151030_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descuento',
            name='url',
        ),
        migrations.AddField(
            model_name='descuento',
            name='funcion',
            field=models.CharField(default=b'Ninguno', max_length=200, verbose_name=b'Funcion a ejecutar'),
        ),
    ]
