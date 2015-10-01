# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0022_auto_20150831_1251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recibo',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Recibo', 'verbose_name_plural': 'Recibos'},
        ),
    ]
