# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aranceles', '0011_auto_20150813_1350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arancel',
            options={'ordering': ['concepto'], 'verbose_name': 'Arancel', 'verbose_name_plural': 'Aranceles'},
        ),
    ]
