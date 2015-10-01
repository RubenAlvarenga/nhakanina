# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finanzas', '0006_auto_20150820_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpago',
            name='created',
            field=models.DateTimeField(default='', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planpago',
            name='created_by',
            field=models.ForeignKey(default='', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planpago',
            name='modified',
            field=models.DateTimeField(default='', auto_now=True),
            preserve_default=False,
        ),
    ]
