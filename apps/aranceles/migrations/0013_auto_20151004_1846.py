# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0012_auto_20150820_1426'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arancel',
            options={'ordering': ['concepto'], 'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Arancel', 'verbose_name_plural': 'Aranceles'},
        ),
        migrations.AlterModelOptions(
            name='concepto',
            options={'ordering': ['tipo_concepto', 'id'], 'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Concepto', 'verbose_name_plural': 'Conceptos'},
        ),
        migrations.AlterModelOptions(
            name='periodo',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Periodo Arancel', 'verbose_name_plural': 'Periodos de Aranceles'},
        ),
        migrations.AlterModelOptions(
            name='tipocarrera',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Tipo Carrera', 'verbose_name_plural': 'Tipos de Carreras'},
        ),
        migrations.AlterModelOptions(
            name='tipocarreraconcepto',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Carrera | Concepto', 'verbose_name_plural': 'Carreras | Conceptos'},
        ),
        migrations.AlterModelOptions(
            name='tipoconcepto',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 'verbose_name': 'Tipo Concepto', 'verbose_name_plural': 'Tipos de Conceptos'},
        ),
    ]
