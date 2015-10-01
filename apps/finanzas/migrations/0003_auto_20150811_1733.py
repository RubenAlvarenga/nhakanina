# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0002_auto_20150809_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleReciboPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='planpago',
            options={'verbose_name': 'Plan de Pago', 'verbose_name_plural': 'Planes'},
        ),
        migrations.AlterModelOptions(
            name='reciboplanpago',
            options={'verbose_name': 'Recibo aplicado a Plan', 'verbose_name_plural': 'Recibos aplicados a Planes'},
        ),
        migrations.AlterField(
            model_name='planpago',
            name='curso_alumno',
            field=models.ForeignKey(verbose_name=b'Curso | Alumno', to='catedras.CursoAlumno'),
        ),
        migrations.AlterField(
            model_name='planpago',
            name='secuencia',
            field=models.DecimalField(default=0, verbose_name=b'Secuencia', max_digits=2, decimal_places=0),
        ),
        migrations.AlterField(
            model_name='reciboplanpago',
            name='plan_pago',
            field=models.ManyToManyField(to='finanzas.PlanPago', through='finanzas.DetalleReciboPlan'),
        ),
        migrations.AddField(
            model_name='detallereciboplan',
            name='plan_pago',
            field=models.ForeignKey(to='finanzas.PlanPago'),
        ),
        migrations.AddField(
            model_name='detallereciboplan',
            name='recibo',
            field=models.ForeignKey(to='finanzas.ReciboPlanPago'),
        ),
    ]
