# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from solo.models import SingletonModel

# Create your models here.
class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Nombre del sitio')
    maintenance_mode = models.BooleanField(default=False)
    acerca = models.TextField('Texto Cadena cacao',null=True, blank=True)
    acerca_footer = models.TextField(null=True, blank=True)
    politica_condicines = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"Configuración del sitio"

    class Meta:
        verbose_name = "Configuración del sitio"

class FotosPortada(models.Model):
    sitio = models.ForeignKey(SiteConfiguration, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    foto = models.FileField(upload_to='fotoportada/')

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Fotos de la portada"

class LinkVideos(models.Model):
    sitio = models.ForeignKey(SiteConfiguration, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    link_video = models.URLField()

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "videos tutoriales"
