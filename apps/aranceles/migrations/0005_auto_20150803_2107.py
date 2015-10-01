# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aranceles', '0004_auto_20150803_2101'),
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
                ('tipo_concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Tipo Concepto', to='aranceles.TipoCarreraConcepto')),
            ],
            options={
                'ordering': ['tipo_concepto', 'id'],
                'verbose_name': 'Concepto',
                'verbose_name_plural': 'Conceptos',
            },
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
            name='concepto',
            unique_together=set([('tipo_concepto', 'concepto')]),
        ),
        migrations.AlterUniqueTogether(
            name='arancel',
            unique_together=set([('resolucion', 'concepto')]),
        ),
    ]
