# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0005_auto_20151030_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descuento',
            name='url',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Url a Ajecutar', blank=True),
        ),
    ]
