# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('autorizaciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Titulo')),
                ('enlace', models.CharField(max_length=200, verbose_name=b'Enlace')),
            ],
            options={
                'verbose_name': 'Enlace',
                'verbose_name_plural': 'Enlaces',
            },
        ),
        migrations.CreateModel(
            name='GrupoMenu',
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
        migrations.CreateModel(
            name='MenuApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100, verbose_name=b'Titulo')),
                ('icono', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'App',
                'verbose_name_plural': 'Apps',
            },
        ),
        migrations.AddField(
            model_name='grupomenu',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'App', to='autorizaciones.MenuApp'),
        ),
        migrations.AddField(
            model_name='enlace',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'Grupo', to='autorizaciones.GrupoMenu'),
        ),
        migrations.AddField(
            model_name='enlace',
            name='permiso',
            field=models.OneToOneField(verbose_name=b'Permiso', to='auth.Permission'),
        ),
        migrations.AlterUniqueTogether(
            name='grupomenu',
            unique_together=set([('app', 'grupo')]),
        ),
        migrations.AlterUniqueTogether(
            name='enlace',
            unique_together=set([('grupo', 'enlace')]),
        ),
    ]
