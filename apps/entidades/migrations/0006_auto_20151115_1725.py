# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0005_persona_socio_afemec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='socio_afemec',
            field=models.BooleanField(default=False, verbose_name=b'Socio AFEMEC'),
        ),
    ]
