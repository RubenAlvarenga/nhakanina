# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0016_auto_20150824_1948'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recibo',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'verbose_name': 'Recibo', 'verbose_name_plural': 'Recibos'},
        ),
    ]
