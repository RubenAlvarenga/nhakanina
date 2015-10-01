# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0023_auto_20150903_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planpago',
            name='authorized_by',
            field=models.ForeignKey(related_name='authorized_finanzas', on_delete=django.db.models.deletion.PROTECT, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name=b'Autorizado por'),
        ),
        migrations.AlterField(
            model_name='planpago',
            name='concepto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Concepto', to='aranceles.Arancel'),
        ),
        migrations.AlterField(
            model_name='planpago',
            name='curso_alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Curso | Alumno', to='catedras.CursoAlumno'),
        ),
        migrations.AlterField(
            model_name='planpago',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Materia', blank=True, to='catedras.Materia', null=True),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='cajero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='concepto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Concepto', to='aranceles.Arancel'),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Persona/Alumno', to='entidades.Persona'),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='usuario_anulacion',
            field=models.ForeignKey(related_name='usuario_anulacion_recibo', on_delete=django.db.models.deletion.PROTECT, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
