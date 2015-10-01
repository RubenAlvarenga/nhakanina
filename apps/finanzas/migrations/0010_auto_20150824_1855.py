# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finanzas', '0009_remove_planpago_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpago',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 24, 18, 54, 58, 558992, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planpago',
            name='created_by',
            field=models.ForeignKey(default=datetime.datetime(2015, 8, 24, 18, 55, 18, 169057, tzinfo=utc), editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planpago',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 24, 18, 55, 36, 977376, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
