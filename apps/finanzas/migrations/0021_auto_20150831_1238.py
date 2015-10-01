# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0020_auto_20150831_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planpago',
            name='materia',
            field=models.ForeignKey(verbose_name=b'Materia', blank=True, to='catedras.Materia', null=True),
        ),
    ]
