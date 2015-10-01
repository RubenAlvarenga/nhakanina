# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finanzas', '0015_auto_20150824_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpago',
            name='authorized_by',
            field=models.ForeignKey(related_name='authorized_finanzas', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Autorizado por'),
        ),
        migrations.AddField(
            model_name='planpago',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 24, 19, 47, 33, 893147, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planpago',
            name='created_by',
            field=models.ForeignKey(default=1, editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planpago',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 24, 19, 48, 10, 235522, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planpago',
            name='observaciones',
            field=models.TextField(null=True, verbose_name=b'Observaciones', blank=True),
        ),
    ]
