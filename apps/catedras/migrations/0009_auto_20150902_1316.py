# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0008_auto_20150831_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carrera',
            options={'ordering': ('tipo', 'grupo', 'nombre'), 'verbose_name': 'Carrera', 'verbose_name_plural': 'Carreras'},
        ),
        migrations.AlterField(
            model_name='cursomateria',
            name='curso',
            field=models.ForeignKey(verbose_name=b'Curso', to='catedras.Curso'),
        ),
        migrations.AlterUniqueTogether(
            name='cursomateria',
            unique_together=set([('curso', 'materia')]),
        ),
    ]
