# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizaciones', '0008_perfil_impresora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='impresora',
            field=models.CharField(max_length=100, verbose_name=b'Impresora'),
        ),
    ]
