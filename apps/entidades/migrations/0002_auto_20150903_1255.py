# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persona',
            options={'ordering': ['apellido1', 'apellido2', 'nombre1'], 'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'persona', 'verbose_name_plural': 'personas'},
        ),
    ]
