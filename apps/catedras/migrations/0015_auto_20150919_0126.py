# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0014_semana'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curso',
            name='dias',
        ),
        migrations.AddField(
            model_name='curso',
            name='dias',
            field=models.ManyToManyField(to='catedras.Semana', verbose_name=b'Dias de Clase'),
        ),
    ]
