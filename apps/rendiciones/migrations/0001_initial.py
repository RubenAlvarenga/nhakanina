# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0027_auto_20151005_1753'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rendicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('nro_rendicion', models.DecimalField(unique=True, verbose_name=b'Nro Rendicion', max_digits=8, decimal_places=0)),
                ('fecha_aprobacion', models.DateField(verbose_name=b'Aprobado el')),
                ('estado', models.CharField(default=b'PEN', max_length=3, verbose_name=b'Estado', choices=[(b'PEN', b'Pendiente'), (b'APR', b'Aprobado')])),
                ('total', models.DecimalField(verbose_name=b'Total', max_digits=10, decimal_places=0)),
                ('aprobado_por', models.ForeignKey(related_name='aprobadopor_rendiciones', on_delete=django.db.models.deletion.PROTECT, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Aprobado por')),
                ('created_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('recibos', models.ManyToManyField(help_text=b'Seleccione los recibos a rendir', to='finanzas.Recibo', verbose_name=b'Recibos a rendir')),
            ],
            options={
                'ordering': ('nro_rendicion',),
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'verbose_name': 'Rendicion',
                'verbose_name_plural': 'Rendiciones',
            },
        ),
    ]
