# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arancel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('fraccionable', models.BooleanField(default=False, verbose_name=b'Fraccionable')),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=8, decimal_places=0)),
            ],
            options={
                'verbose_name': 'Arancel',
                'verbose_name_plural': 'Aranceles',
            },
        ),
        migrations.CreateModel(
            name='Concepto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('concepto', models.CharField(max_length=255, verbose_name=b'Titulo')),
                ('estado', models.BooleanField(default=True, verbose_name=b'Activo')),
            ],
            options={
                'ordering': ['tipoConcepto', 'id'],
                'verbose_name': 'Concepto',
                'verbose_name_plural': 'Conceptos',
            },
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('resolucion', models.CharField(unique=True, max_length=8, verbose_name=b'Resolucion')),
                ('inicio', models.DateField(verbose_name=b'Inicio')),
                ('fin', models.DateField(null=True, verbose_name=b'Fin', blank=True)),
                ('estado', models.CharField(default=b'ACT', unique=True, max_length=3, choices=[(b'ACT', b'Activo'), (b'HIS', b'Historico')])),
                ('created_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Periodo Arancel',
                'verbose_name_plural': 'Periodos de Aranceles',
            },
        ),
        migrations.CreateModel(
            name='TipoCarrera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=255, verbose_name=b'Titulo')),
            ],
            options={
                'verbose_name': 'Tipo Carrera',
                'verbose_name_plural': 'Tipos de Carreras',
            },
        ),
        migrations.CreateModel(
            name='TipoCarreraConcepto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipoCarrera', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Tipo Carrera', to='aranceles.TipoCarrera')),
            ],
            options={
                'verbose_name': 'Carrera | Concepto',
                'verbose_name_plural': 'Carreras | Conceptos',
            },
        ),
        migrations.CreateModel(
            name='TipoConcepto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=255, verbose_name=b'Titulo')),
            ],
            options={
                'verbose_name': 'Tipo Concepto',
                'verbose_name_plural': 'Tipos de Conceptos',
            },
        ),
        migrations.AddField(
            model_name='tipocarreraconcepto',
            name='tipoConcepto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Tipo Concepto', to='aranceles.TipoConcepto'),
        ),
        migrations.AddField(
            model_name='concepto',
            name='tipoConcepto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Tipo Concepto', to='aranceles.TipoCarreraConcepto'),
        ),
        migrations.AddField(
            model_name='arancel',
            name='concepto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Concepto', to='aranceles.Concepto'),
        ),
        migrations.AddField(
            model_name='arancel',
            name='created_by',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='arancel',
            name='resolucion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Resolucion', to='aranceles.Periodo'),
        ),
        migrations.AlterUniqueTogether(
            name='tipocarreraconcepto',
            unique_together=set([('tipoCarrera', 'tipoConcepto')]),
        ),
        migrations.AlterUniqueTogether(
            name='concepto',
            unique_together=set([('tipoConcepto', 'concepto')]),
        ),
        migrations.AlterUniqueTogether(
            name='arancel',
            unique_together=set([('resolucion', 'concepto')]),
        ),
    ]
