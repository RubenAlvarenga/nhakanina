# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autorizaciones', '0002_auto_20150825_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agrupador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grupo', models.CharField(max_length=100, verbose_name=b'Grupo')),
                ('icono', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Grupo Menu',
                'verbose_name_plural': 'Grupos de Menus',
            },
        ),
        migrations.AlterUniqueTogether(
            name='grupomenu',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='grupomenu',
            name='app',
        ),
        migrations.AddField(
            model_name='enlace',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default='', verbose_name=b'App', to='autorizaciones.MenuApp'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='enlace',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Grupo', to='autorizaciones.Agrupador'),
        ),
        migrations.AlterUniqueTogether(
            name='enlace',
            unique_together=set([('app', 'grupo', 'enlace')]),
        ),
        migrations.DeleteModel(
            name='GrupoMenu',
        ),
    ]
