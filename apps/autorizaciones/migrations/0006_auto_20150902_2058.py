# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizaciones', '0005_menuapp_app_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enlace',
            name='permiso',
            field=models.ForeignKey(verbose_name=b'Permiso', to='auth.Permission'),
        ),
        migrations.AlterField(
            model_name='menuapp',
            name='app_name',
            field=models.CharField(default='', unique=True, max_length=100, verbose_name=b'App Name'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='enlace',
            unique_together=set([]),
        ),
    ]
