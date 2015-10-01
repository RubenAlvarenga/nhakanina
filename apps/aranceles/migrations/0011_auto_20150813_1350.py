# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0010_arancel_fraccionable_hasta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arancel',
            name='fraccionable',
        ),
        migrations.RemoveField(
            model_name='arancel',
            name='fraccionable_hasta',
        ),
        migrations.AddField(
            model_name='concepto',
            name='fraccionable',
            field=models.BooleanField(default=False, verbose_name=b'Fraccionable'),
        ),
        migrations.AddField(
            model_name='concepto',
            name='fraccionable_hasta',
            field=models.DecimalField(null=True, verbose_name=b'hasta', max_digits=2, decimal_places=0, blank=True),
        ),
        migrations.AddField(
            model_name='concepto',
            name='funcion',
            field=models.CharField(help_text=b'Funcion especial para calculos de cobro', max_length=255, null=True, verbose_name=b'Funcion', blank=True),
        ),
    ]
