# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0016_arancel_activo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='periodo',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Periodo', 'verbose_name_plural': 'Periodos de Aranceles'},
        ),
        migrations.AlterModelOptions(
            name='tipoconcepto',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'TipoConcepto', 'verbose_name_plural': 'Tipos de Conceptos'},
        ),
    ]
