# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aranceles', '0009_auto_20150803_2140'),
        ('entidades', '0001_initial'),
        ('finanzas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateTimeField(verbose_name=b'Fecha')),
                ('nro_recibo', models.DecimalField(verbose_name=b'Nro Recibo', max_digits=8, decimal_places=0)),
                ('serie', models.CharField(default=b'I', max_length=1, verbose_name=b'Serie')),
                ('estado', models.CharField(default=b'PRO', max_length=3, verbose_name=b'Estado', choices=[(b'PRO', b'Procesado'), (b'ANU', b'Anulado')])),
                ('cantidad', models.DecimalField(verbose_name=b'Cantidad', max_digits=3, decimal_places=0)),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=10, decimal_places=0)),
                ('rendido', models.BooleanField(default=False, verbose_name=b'Rendido', editable=False)),
            ],
            options={
                'verbose_name': 'Recibo',
                'verbose_name_plural': 'Recibos',
            },
        ),
        migrations.AlterField(
            model_name='planpago',
            name='vencimiento',
            field=models.DateField(null=True, verbose_name=b'Fecha de Vencimiento', blank=True),
        ),
        migrations.CreateModel(
            name='ReciboPlanPago',
            fields=[
                ('recibo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='finanzas.Recibo')),
                ('plan_pago', models.ManyToManyField(to='finanzas.PlanPago')),
            ],
            options={
                'abstract': False,
            },
            bases=('finanzas.recibo',),
        ),
        migrations.AddField(
            model_name='recibo',
            name='cajero',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recibo',
            name='concepto',
            field=models.ForeignKey(verbose_name=b'Concepto', to='aranceles.Arancel'),
        ),
        migrations.AddField(
            model_name='recibo',
            name='persona',
            field=models.ForeignKey(verbose_name=b'Persona/Alumno', to='entidades.Persona'),
        ),
        migrations.AlterUniqueTogether(
            name='recibo',
            unique_together=set([('nro_recibo', 'serie')]),
        ),
    ]
