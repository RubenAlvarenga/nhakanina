# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0021_auto_20150831_1238'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='planpago',
            unique_together=set([('curso_alumno', 'concepto', 'secuencia', 'materia')]),
        ),
    ]
