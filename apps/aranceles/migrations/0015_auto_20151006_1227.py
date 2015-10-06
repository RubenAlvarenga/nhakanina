# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0014_auto_20151005_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='estado',
            field=models.CharField(default=b'ACT', max_length=3, choices=[(b'ACT', b'Activo'), (b'HIS', b'Historico')]),
        ),
    ]
