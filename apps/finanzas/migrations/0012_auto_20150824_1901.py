# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0011_auto_20150824_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planpago',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='planpago',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
