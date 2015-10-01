# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0009_auto_20150803_2140'),
        ('catedras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inicio', models.DateField(verbose_name=b'Inicio')),
                ('fin', models.DateField(null=True, verbose_name=b'Fin', blank=True)),
                ('dias', models.CharField(help_text=b'Dias de clase Ej.:[Lun, Mie / Vie]', max_length=100, verbose_name=b'Dias')),
                ('turno', models.CharField(max_length=100, verbose_name=b'Turno - Seccion')),
                ('fecha_tope_matriculacion', models.DateField(help_text=b'Para calcular el monto de la Matricula [*Si Aplica]', null=True, verbose_name=b'Fecha tope de Matriculacion', blank=True)),
                ('cantidad_cuotas', models.DecimalField(help_text=b'Importante para generar plan de pagos', verbose_name=b'Cantidad de Cuotas', max_digits=2, decimal_places=0)),
                ('estado', models.BooleanField(default=True, verbose_name=b'Habilitado')),
                ('aranceles', models.ManyToManyField(related_name='arancel_aranceles', verbose_name=b'Aranceles Aplicables', to='aranceles.Arancel')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Carrera', to='catedras.Carrera')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Matricula Normal', to='aranceles.Arancel', help_text=b'Periodo Ordinario de Matriculacion')),
                ('matricula_fpo', models.ForeignKey(related_name='arancel_matricula_fpo', on_delete=django.db.models.deletion.PROTECT, blank=True, to='aranceles.Arancel', help_text=b'Fuera del Periodo Ordinario de Matriculacion [*Si Aplica]', null=True, verbose_name=b'Matricula FPO')),
                ('monto_cuota', models.ForeignKey(related_name='arancel_monto_cuota', verbose_name=b'Monto Cuota', to='aranceles.Arancel')),
            ],
            options={
                'verbose_name': 'curso',
                'verbose_name_plural': 'cursos',
            },
        ),
    ]
