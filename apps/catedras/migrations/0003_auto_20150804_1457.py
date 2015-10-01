# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0002_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='dias',
            field=models.CharField(help_text=b'Dias de clase Ej.:[Lun, Mie, Vie]', max_length=100, verbose_name=b'Dias'),
        ),
    ]
