# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0001_initial'),
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
            name='tipoConcepto',
        ),
        migrations.AlterUniqueTogether(
            name='tipocarreraconcepto',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tipocarreraconcepto',
            name='tipoCarrera',
        ),
        migrations.RemoveField(
            model_name='tipocarreraconcepto',
            name='tipoConcepto',
        ),
        migrations.DeleteModel(
            name='Arancel',
        ),
        migrations.DeleteModel(
            name='Concepto',
        ),
        migrations.DeleteModel(
            name='TipoCarreraConcepto',
        ),
    ]
