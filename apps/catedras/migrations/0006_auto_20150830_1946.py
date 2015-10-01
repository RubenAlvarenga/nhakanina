# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0012_auto_20150820_1426'),
        ('catedras', '0005_auto_20150830_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='CursoMateria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Curso Materia',
                'verbose_name_plural': 'Cursos/Materias',
            },
        ),
        migrations.AddField(
            model_name='curso',
            name='examen_extra',
            field=models.ManyToManyField(related_name='arancel_examen_extra', verbose_name=b'Otros Examenes', to='aranceles.Arancel'),
        ),
        migrations.AddField(
            model_name='curso',
            name='examen_ordinario',
            field=models.ForeignKey(related_name='arancel_examen_ordinario', on_delete=django.db.models.deletion.PROTECT, default='', verbose_name=b'Monto Examen Ordinario', to='aranceles.Arancel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cursomateria',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Curso', to='catedras.Curso'),
        ),
        migrations.AddField(
            model_name='cursomateria',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Materia', to='catedras.Materia'),
        ),
        migrations.AddField(
            model_name='curso',
            name='materias',
            field=models.ManyToManyField(to='catedras.Materia', through='catedras.CursoMateria'),
        ),
    ]
