# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autorizaciones', '0007_auto_20150909_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='impresora',
            field=models.CharField(default=b'ninguno', max_length=200, verbose_name=b'Impresora', choices=[(b'ninguno', b'Ninguno'), (b'es_socio_afemec', b'Socio de AFEMEC'), (b'es_docente_ise', b'Docente del ISE')]),
        ),
    ]
