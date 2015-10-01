# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0008_auto_20150824_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planpago',
            name='created_by',
        ),
    ]
