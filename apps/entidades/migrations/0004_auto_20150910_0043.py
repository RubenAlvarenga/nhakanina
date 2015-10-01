# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0003_auto_20150903_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='fecha_nacimiento',
            field=models.DateField(null=True, verbose_name=b'Nacimiento', blank=True),
        ),
    ]
