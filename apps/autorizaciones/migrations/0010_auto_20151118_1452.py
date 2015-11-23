# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizaciones', '0009_auto_20151118_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='impresora',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Impresora', blank=True),
        ),
    ]
