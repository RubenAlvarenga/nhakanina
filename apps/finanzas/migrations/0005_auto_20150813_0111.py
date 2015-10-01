# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0004_auto_20150811_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibo',
            name='fecha',
            field=models.DateField(verbose_name=b'Fecha'),
        ),
    ]
