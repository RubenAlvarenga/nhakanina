# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0015_auto_20151006_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='arancel',
            name='activo',
            field=models.BooleanField(default=True, verbose_name=b'Activo'),
        ),
    ]
