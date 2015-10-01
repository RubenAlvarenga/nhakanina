# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0017_auto_20150825_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='observaciones',
            field=models.TextField(null=True, verbose_name=b'Observaciones', blank=True),
        ),
    ]
