# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0004_auto_20150806_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Nombre')),
            ],
            options={
                'verbose_name': 'Materia',
                'verbose_name_plural': 'Materias',
            },
        ),
        migrations.AlterField(
            model_name='curso',
            name='monto_cuota',
            field=models.ForeignKey(related_name='arancel_monto_cuota', on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Monto Cuota', to='aranceles.Arancel'),
        ),
        migrations.AlterField(
            model_name='cursoalumno',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Alumno', to='entidades.Alumno'),
        ),
        migrations.AlterField(
            model_name='cursoalumno',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Carrera - Curso', to='catedras.Curso'),
        ),
    ]
