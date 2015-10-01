# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0009_auto_20150803_2140'),
        ('catedras', '0004_auto_20150806_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secuencia', models.DecimalField(verbose_name=b'Secuencia', max_digits=2, decimal_places=0)),
                ('vencimiento', models.DateField(verbose_name=b'Fecha de Vencimiento')),
                ('estado', models.CharField(default=b'PEN', max_length=3, verbose_name=b'Estado', choices=[(b'PEN', b'Pendiente'), (b'PAG', b'Pagado'), (b'ANU', b'Anulado')])),
                ('monto', models.DecimalField(verbose_name=b'Monto', max_digits=9, decimal_places=0)),
                ('concepto', models.ForeignKey(verbose_name=b'Concepto', to='aranceles.Arancel')),
                ('curso_alumno', models.ForeignKey(verbose_name=b'Alumno', to='catedras.CursoAlumno')),
            ],
            options={
                'verbose_name': 'Plan de Pago',
                'verbose_name_plural': 'Planes de Pago',
            },
        ),
        migrations.AlterUniqueTogether(
            name='planpago',
            unique_together=set([('curso_alumno', 'concepto', 'secuencia')]),
        ),
    ]
