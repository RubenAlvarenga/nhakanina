# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.thumbs
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', apps.thumbs.ImageWithThumbsField(null=True, upload_to=b'avatar_user/', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfiles',
            },
        ),
    ]
