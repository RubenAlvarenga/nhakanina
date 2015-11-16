# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0007_auto_20151104_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descuento',
            name='funcion',
            field=models.CharField(default=b'ninguno', max_length=200, verbose_name=b'Condiciones', choices=[(b'ninguno', b'Ninguno'), (b'es_socio_afemec', b'Socio de AFEMEC'), (b'es_docente_ise', b'Docente del ISE')]),
        ),
    ]
