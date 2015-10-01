# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizaciones', '0004_menuapp_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuapp',
            name='app_name',
            field=models.CharField(max_length=100, unique=True, null=True, verbose_name=b'App Name', blank=True),
        ),
    ]
