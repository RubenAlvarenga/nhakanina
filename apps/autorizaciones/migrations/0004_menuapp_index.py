# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizaciones', '0003_auto_20150825_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuapp',
            name='index',
            field=models.CharField(default='', max_length=200, verbose_name=b'Index'),
            preserve_default=False,
        ),
    ]
