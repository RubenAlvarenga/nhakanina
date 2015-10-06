# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0013_auto_20151004_1846'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='periodo',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'PeriodoArancel', 'verbose_name_plural': 'Periodos de Aranceles'},
        ),
    ]
