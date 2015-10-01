# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0003_auto_20150803_2055'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='arancel',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='arancel',
            name='concepto',
        ),
        migrations.RemoveField(
            model_name='arancel',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='arancel',
            name='resolucion',
        ),
        migrations.AlterUniqueTogether(
            name='concepto',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='concepto',
            name='tipo_concepto',
        ),
        migrations.DeleteModel(
            name='Arancel',
        ),
        migrations.DeleteModel(
            name='Concepto',
        ),
    ]
