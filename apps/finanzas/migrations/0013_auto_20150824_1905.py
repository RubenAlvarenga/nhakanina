# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0012_auto_20150824_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planpago',
            name='created',
        ),
        migrations.RemoveField(
            model_name='planpago',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='planpago',
            name='modified',
        ),
        migrations.AlterField(
            model_name='recibo',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
