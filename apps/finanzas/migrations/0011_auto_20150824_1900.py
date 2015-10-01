# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0010_auto_20150824_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planpago',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
