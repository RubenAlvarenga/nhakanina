# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0006_auto_20151115_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='docente_ise',
            field=models.BooleanField(default=False, verbose_name=b'Docente ISE'),
        ),
    ]
