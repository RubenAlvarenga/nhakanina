# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0016_arancel_activo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('descuentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('motivo', models.CharField(max_length=100, verbose_name=b'Motivo')),
                ('estado', models.CharField(default=b'ACT', max_length=3, verbose_name=b'Estado', choices=[(b'ACT', b'Activo'), (b'HIS', b'Historico')])),
                ('cant_minima_concepto', models.DecimalField(verbose_name=b'Cantidad Minima', max_digits=2, decimal_places=0)),
                ('cant_maxima_concepto', models.DecimalField(verbose_name=b'Cantidad Maxima', max_digits=3, decimal_places=0)),
                ('porcentaje', models.DecimalField(verbose_name=b'Porcentaje', max_digits=2, decimal_places=0)),
                ('url', models.CharField(max_length=200, verbose_name=b'Url a Ajecutar')),
                ('created_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('tipo_carrera_concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Tipo Carrera | Concepto', to='aranceles.TipoCarreraConcepto')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'verbose_name': 'Descuento',
                'verbose_name_plural': 'Descuentos',
            },
        ),
        migrations.RemoveField(
            model_name='portipocarreraconcepto',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='portipocarreraconcepto',
            name='tipoConcepto',
        ),
        migrations.DeleteModel(
            name='PorTipoCarreraConcepto',
        ),
    ]
