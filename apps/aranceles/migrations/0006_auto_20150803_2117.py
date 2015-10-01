# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0005_auto_20150803_2107'),
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
        migrations.RemoveField(
            model_name='periodo',
            name='created_by',
        ),
        migrations.AlterUniqueTogether(
            name='tipocarreraconcepto',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='tipocarreraconcepto',
            name='tipo_carrera',
        ),
        migrations.RemoveField(
            model_name='tipocarreraconcepto',
            name='tipo_concepto',
        ),
        migrations.DeleteModel(
            name='Arancel',
        ),
        migrations.DeleteModel(
            name='Concepto',
        ),
        migrations.DeleteModel(
            name='Periodo',
        ),
        migrations.DeleteModel(
            name='TipoCarrera',
        ),
        migrations.DeleteModel(
            name='TipoCarreraConcepto',
        ),
        migrations.DeleteModel(
            name='TipoConcepto',
        ),
    ]
