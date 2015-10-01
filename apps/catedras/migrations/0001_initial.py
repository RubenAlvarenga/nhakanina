# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0009_auto_20150803_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Nombre')),
                ('duracion', models.DecimalField(help_text=b'En meses', verbose_name=b'Duracion', max_digits=2, decimal_places=0, blank=True)),
            ],
            options={
                'verbose_name': 'Carrera',
                'verbose_name_plural': 'Carreras',
            },
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grupo', models.CharField(max_length=100, verbose_name=b'Grupo')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.AddField(
            model_name='carrera',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Grupo', blank=True, to='catedras.Grupo', null=True),
        ),
        migrations.AddField(
            model_name='carrera',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Tipo Carrera', to='aranceles.TipoCarrera'),
        ),
    ]
