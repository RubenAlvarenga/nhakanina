# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0027_auto_20151005_1753'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planpago',
            options={'ordering': ['-estado', '-id'], 'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Plan de Pago', 'verbose_name_plural': 'Planes'},
        ),
        migrations.AlterField(
            model_name='planpago',
            name='estado',
            field=models.CharField(default=b'PEN', max_length=3, verbose_name=b'Estado', choices=[(b'PEN', b'Pendiente'), (b'PAG', b'Pagado'), (b'ANU', b'Anulado'), (b'EXO', b'Exonerado')]),
        ),
    ]
