# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entidades', '0001_initial'),
        ('catedras', '0003_auto_20150804_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='CursoAlumno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('fecha_inscripcion', models.DateField(verbose_name=b'Fecha de Inscripci\xc3\xb3n')),
                ('estado', models.CharField(default=b'ACT', max_length=3, verbose_name=b'Estado', choices=[(b'ACT', b'Activo'), (b'HIS', b'Historico')])),
                ('observacion', models.TextField(null=True, verbose_name=b'Observaciones', blank=True)),
                ('alumno', models.ForeignKey(verbose_name=b'Alumno', to='entidades.Alumno')),
                ('created_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('curso', models.ForeignKey(verbose_name=b'Carrera - Curso', to='catedras.Curso')),
            ],
            options={
                'verbose_name': 'Curso | Lista de Alumnos',
                'verbose_name_plural': 'Cursos | Listados de Alumnos',
            },
        ),
        migrations.AlterUniqueTogether(
            name='cursoalumno',
            unique_together=set([('curso', 'alumno')]),
        ),
    ]
