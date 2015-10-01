# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0007_auto_20150831_0020'),
        ('finanzas', '0019_auto_20150828_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpago',
            name='materia',
            field=models.ForeignKey(verbose_name=b'Materia', blank=True, to='catedras.CursoMateria', null=True),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='fecha_anulacion',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
    ]
