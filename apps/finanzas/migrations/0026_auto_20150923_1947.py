# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0025_auto_20150914_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planpago',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Plan de Pago', 'verbose_name_plural': 'Planes'},
        ),
    ]
