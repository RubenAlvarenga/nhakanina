# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catedras', '0017_curso_turnos'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='etapa',
            field=models.DecimalField(null=True, verbose_name=b'Etapa', max_digits=2, decimal_places=0, blank=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='tipo_periodo',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name=b'Tipo Periodo', choices=[(b'ANU', b'Anual'), (b'SEM', b'Semestral')]),
        ),
    ]
