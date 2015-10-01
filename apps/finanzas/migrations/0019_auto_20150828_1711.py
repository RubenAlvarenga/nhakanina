# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finanzas', '0018_recibo_observaciones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibo',
            name='observaciones',
        ),
        migrations.AddField(
            model_name='recibo',
            name='fecha_anulacion',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='recibo',
            name='motivo_anulacion',
            field=models.TextField(null=True, verbose_name=b'Motivo Anulacion', blank=True),
        ),
        migrations.AddField(
            model_name='recibo',
            name='usuario_anulacion',
            field=models.ForeignKey(related_name='usuario_anulacion_recibo', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
