# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0013_auto_20150913_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semana',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre')),
            ],
            options={
                'verbose_name': 'Semana',
                'verbose_name_plural': 'Semanas',
            },
        ),
    ]
