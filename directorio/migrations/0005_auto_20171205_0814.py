# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 14:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('directorio', '0004_auto_20171123_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opcion', models.CharField(choices=[('Web', 'Web'), ('Facebook', 'Facebook'), ('Twitter', 'Twitter'), ('Youtube', 'Youtube'), ('Google+', 'Google+'), ('Instagram', 'Instagram'), ('Linkedin', 'Linkedin'), ('Flickr', 'Flickr'), ('Pinterest', 'Pinterest'), ('Otra', 'Otra')], max_length=25)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='organizacion',
            name='ciudad',
            field=models.CharField(blank=True, help_text='Cuidad donde esta ubicada o direcci\xf3n', max_length=255, null=True, verbose_name='Ciudad/Direcci\xf3n'),
        ),
        migrations.AlterField(
            model_name='organizacion',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Las dimenciones de la imagen son 200x200', null=True, upload_to='logos/'),
        ),
        migrations.AddField(
            model_name='redes',
            name='organizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directorio.Organizacion'),
        ),
    ]