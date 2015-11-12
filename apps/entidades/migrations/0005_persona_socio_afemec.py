# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0004_auto_20150910_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='socio_afemec',
            field=models.BooleanField(default=False, verbose_name=b'Socio Afemec'),
        ),
    ]
