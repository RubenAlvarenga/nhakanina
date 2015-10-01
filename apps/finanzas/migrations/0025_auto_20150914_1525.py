# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0024_auto_20150904_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planpago',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
