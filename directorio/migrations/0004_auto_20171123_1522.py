# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directorio', '0003_auto_20171121_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizacion',
            name='tipo_actividad',
        ),
        migrations.AddField(
            model_name='organizacion',
            name='tipo_actividad',
            field=models.ManyToManyField(to='directorio.TipoActividad', verbose_name='Tipo de Actividad'),
        ),
    ]