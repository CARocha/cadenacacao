# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-06-18 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='acerca_footer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='politica_condicines',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='acerca',
            field=models.TextField(blank=True, null=True, verbose_name='Texto Cadena cacao'),
        ),
    ]
