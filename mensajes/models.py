# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from directorio.models import Pais, TIPO_CHOICES, Participacion, Organizacion
# Create your models here.

class Mensaje(models.Model):
    pais = models.ManyToManyField(Pais, blank=True)
    tipo_organizacion = models.CharField(max_length=20, choices=TIPO_CHOICES, null=True, blank=True)
    participacion_cadena = models.ManyToManyField(Participacion, blank=True)
    destinatario = models.ManyToManyField(Organizacion, blank=True)
    asunto = models.CharField(max_length=300)
    contenido = models.TextField()

    usuario = models.ForeignKey(User)

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"

    def __str__(self):
        return self.asunto
    