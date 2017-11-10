# -*- coding: UTF-8 -*-
from django.db import models
from .models import *
from django import forms

def paises():
	foo = Organizacion.objects.order_by('pais_sede').distinct().values_list('pais_sede__id', flat=True)
	return Pais.objects.filter(id__in=foo)

def paises_labora():
	foo = Organizacion.objects.order_by('paises_labora').distinct().values_list('paises_labora__id', flat=True)
	return Pais.objects.filter(id__in=foo)

AMBITO_CHOICES = (
		('','Seleccione ámbito de acción'),('Internacional','Internacional'),('Regional','Regional'),
		('Nacional','Nacional'),('Local','Local')
	)

TIPO_CHOICES = (
		('Sector publico','Sector público'),('Sector privado','Sector privado'),('Academia','Academia'),
		('Asociacion','Asociación'),('Cooperativa','Cooperativa'),('Fundacion','Fundación'),
		('ONG','ONG'),('ONGI','ONGI'),('Plataforma','Plataforma')
	)

ESP_ORG_CHOICES = (('','Seleccione tipo'),
	('Organizacion','Organización'),('Especialista','Especialista'))

class OrganizacionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(OrganizacionForm, self).__init__(*args, **kwargs)
		self.fields['pais_sede'] = forms.ModelChoiceField(queryset=paises(),required=True)
		self.fields['ambito_accion'] = forms.ChoiceField(choices=AMBITO_CHOICES,required=False)
		self.fields['tipo_organizacion'] = forms.MultipleChoiceField(choices=TIPO_CHOICES,required=False)
		self.fields['paises_labora'] = forms.ModelMultipleChoiceField(queryset=paises_labora(),required=False)
		self.fields['participacion_cadena'] = forms.ModelMultipleChoiceField(queryset=Participacion.objects.all(),required=False)
		self.fields['servicios'] = forms.ModelMultipleChoiceField(queryset=ServiciosCadena.objects.all(),required=False)
		self.fields['intercambio'] = forms.ModelMultipleChoiceField(queryset=IntercambioTecnologia.objects.all(),required=False)
		self.fields['tipo'] = forms.ChoiceField(choices=ESP_ORG_CHOICES,required=False)

class BuscadorForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(BuscadorForm, self).__init__(*args, **kwargs)
		self.fields['q'] = forms.CharField()

class OrgForm(forms.ModelForm):
	class Meta:
		model = Organizacion
		fields = '__all__'
		exclude = ['usuario',]

class ProductosServiciosFrom(forms.ModelForm):
	class Meta:
		model = ProductosServicios
		fields = '__all__'
		exclude = ['organizacion',]

class EmailForm(forms.Form):
      mensaje = forms.CharField(widget=forms.Textarea,label="Descripción breve")

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','email','first_name', 'last_name',)