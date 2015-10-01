# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizaciones', '0006_auto_20150902_2058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perfil',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'perfil', 'verbose_name_plural': 'perfiles'},
        ),
    ]
