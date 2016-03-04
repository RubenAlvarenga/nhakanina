# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0016_turno'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='turnos',
            field=models.ManyToManyField(to='catedras.Turno', verbose_name=b'Turnos'),
        ),
    ]
