# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentos', '0003_recibodescuento'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReciboDescuento',
        ),
    ]
