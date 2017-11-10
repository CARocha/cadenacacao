# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from location_field.models.plain import PlainLocationField
from sorl.thumbnail import ImageField
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class Pais(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = 'País'
		verbose_name_plural = 'Paises'

@python_2_unicode_compatible
class TipoActividad(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = 'Tipo de actividad'
		verbose_name_plural = 'Tipos de actividades'

@python_2_unicode_compatible
class Participacion(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name_plural = 'Participación en la cadena de valor'

@python_2_unicode_compatible
class ServiciosCadena(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name_plural = 'Servicios en la Cadena de Valor'

@python_2_unicode_compatible
class IntercambioTecnologia(models.Model):
	nombre = models.CharField(max_length=255)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name_plural = 'Intercambio de Tecnología'

TIPO_CHOICES = (
		('Sector publico','Sector público'),('Sector privado','Sector privado'),('Academia','Academia'),
		('Asociacion','Asociación'),('Cooperativa','Cooperativa'),('Fundacion','Fundación'),
		('ONG','ONG'),('ONGI','ONGI'),('Plataforma','Plataforma')
	)

AMBITO_CHOICES = (
		('Internacional','Internacional'),('Regional','Regional'),
		('Nacional','Nacional'),('Local','Local')
	)

PERIODO_CHOICES = (
		('2 años','2 años'),('3 años','3 años'),
		('4 años','4 años'),('5 años','5 años'),
		('Más de 5 años','Más de 5 años')
	)

ESP_ORG_CHOICES = (
	('Organizacion','Organización'),('Especialista','Especialista'))

@python_2_unicode_compatible
class Organizacion(models.Model):
	tipo = models.CharField(max_length=20,choices=ESP_ORG_CHOICES)
	nombre = models.CharField(max_length=255)
	logo = ImageField(upload_to='logos/',blank=True,null=True)
	objetivo = models.TextField()
	contacto_1 = models.CharField(max_length=255,blank=True,null=True,verbose_name='Persona de Contacto 1')
	correo_1 = models.CharField(max_length=255,blank=True,null=True,verbose_name='Correo 1')
	telefono_1 = models.CharField(max_length=255,blank=True,null=True,verbose_name='Teléfono 1')
	contacto_2 = models.CharField(max_length=255,blank=True,null=True,verbose_name='Persona de Contacto 2')
	correo_2 = models.CharField(max_length=255,blank=True,null=True,verbose_name='Correo 2')
	telefono_2 = models.CharField(max_length=255,blank=True,null=True,verbose_name='Teléfono 2')
	pais_sede = models.ForeignKey(Pais,verbose_name='País Sede')
	ciudad = models.CharField(max_length=255,blank=True,null=True,help_text='Cuidad donde esta ubicada')
	location = PlainLocationField(based_fields=['ciudad'], zoom=5,blank=True,null=True,verbose_name='Ubicación')
	tipo_organizacion = models.CharField(max_length=20,choices=TIPO_CHOICES,verbose_name='Tipo de Organización')
	tipo_actividad = models.ForeignKey(TipoActividad,verbose_name='Tipo de Actividad')
	participacion_cadena = models.ManyToManyField(Participacion,verbose_name='Participación en la Cadena de Valor')
	servicios = models.ManyToManyField(ServiciosCadena,verbose_name='Servicios  en la Cadena de Valor')
	ambito_accion = models.CharField(max_length=20,choices=AMBITO_CHOICES,verbose_name='Ámbito de Acción')
	paises_labora = models.ManyToManyField(Pais,related_name='Paises',verbose_name='Países donde Labora')
	cobertura = models.CharField(max_length=255,verbose_name='Cobertura Geográfica')
	periodo_permanencia = models.CharField(max_length=20,choices=PERIODO_CHOICES,verbose_name='Período de Permanencia')
	intercambio = models.ManyToManyField(IntercambioTecnologia,verbose_name='Intercambio de Tecnología')
	sitio_web = models.URLField(blank=True,null=True)
	miembros = models.IntegerField(blank=True,null=True,verbose_name='N° de Miembros/Socio')
	tamano = models.CharField(max_length=20,blank=True,null=True,verbose_name='Tamaño')
	actualizado = models.DateField(editable=False,auto_now=True)
	slug = models.SlugField(editable=False, max_length=450)
	ratings = GenericRelation(Rating, related_query_name='orgs')
	usuario = models.ForeignKey(User,blank=True,null=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nombre)
		super(Organizacion, self).save(*args, **kwargs)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = 'Organización/Especialista'
		verbose_name_plural = 'Organizaciones/Especialistas'

class ProductosServicios(models.Model):
	organizacion = models.ForeignKey(Organizacion)
	nombre = models.CharField(max_length=255)
	foto = ImageField(upload_to='productos-servicios/')

	class Meta:
		verbose_name = 'Producto/Servicio'
		verbose_name_plural = 'Productos y Servicios'
