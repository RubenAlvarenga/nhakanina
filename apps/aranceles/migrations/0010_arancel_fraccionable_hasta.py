# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0009_auto_20150803_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='arancel',
            name='fraccionable_hasta',
            field=models.DecimalField(null=True, verbose_name=b'hasta', max_digits=2, decimal_places=0, blank=True),
        ),
    ]
