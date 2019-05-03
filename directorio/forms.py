# -*- coding: UTF-8 -*-
from django.db import models
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

def paises():
	foo = Organizacion.objects.order_by('pais_sede').distinct().values_list('pais_sede__id', flat=True)
	return Pais.objects.filter(id__in=foo)

def paises_labora():
	foo = Organizacion.objects.order_by('paises_labora').distinct().values_list('paises_labora__id', flat=True)
	return Pais.objects.filter(id__in=foo)

AMBITO_CHOICES = (
		('','------'),('Internacional','Internacional'),('Regional','Regional'),
		('Nacional','Nacional'),('Local','Local')
	)

TIPO_CHOICES = (
		('Sector publico','Sector público'),('Sector privado','Sector privado'),('Academia','Academia'),
		('Asociacion','Asociación'),('Cooperativa','Cooperativa'),('Fundacion','Fundación'),
		('ONG','ONG'),('ONGI','ONGI'),('Plataforma','Plataforma'),('Consultor','Consultor')
	)

# ESP_ORG_CHOICES = (('','Seleccione'),
# 	('Organizacion','Organización'),('Especialista','Especialista'))

class OrganizacionForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(OrganizacionForm, self).__init__(*args, **kwargs)
		self.fields['pais_sede'] = forms.ModelChoiceField(queryset=paises(),required=True)
		self.fields['ambito_accion'] = forms.ChoiceField(choices=AMBITO_CHOICES,required=False)
		self.fields['tipo_organizacion'] = forms.MultipleChoiceField(choices=TIPO_CHOICES,required=False)
		self.fields['paises_labora'] = forms.ModelMultipleChoiceField(queryset=paises_labora(),required=False)
		self.fields['participacion_cadena'] = forms.ModelMultipleChoiceField(queryset=Participacion.objects.all(),required=False)
		self.fields['servicios'] = forms.ModelMultipleChoiceField(queryset=ServiciosCadena.objects.all(),required=False)
		# self.fields['intercambio'] = forms.ModelMultipleChoiceField(queryset=IntercambioTecnologia.objects.all(),required=False)
		# self.fields['tipo'] = forms.ChoiceField(choices=ESP_ORG_CHOICES,required=False)
		self.fields['tipo_actividad'] = forms.ModelMultipleChoiceField(queryset=TipoActividad.objects.all(),required=False)

class BuscadorForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(BuscadorForm, self).__init__(*args, **kwargs)
		self.fields['q'] = forms.CharField()

class OrgForm(forms.ModelForm):
	objetivo = forms.CharField(label='Descripción de la Organización',max_length=3000,widget=CKEditorUploadingWidget)
	class Meta:
		model = Organizacion
		fields = '__all__'
		exclude = ['usuario',]


class ProductosServiciosFrom(forms.ModelForm):
	nombre = models.CharField(max_length=30)
	class Meta:
		model = ProductosServicios
		fields = '__all__'
		exclude = ['organizacion',]

class RedesFrom(forms.ModelForm):
	class Meta:
		model = Redes
		fields = '__all__'
		exclude = ['organizacion',]

class EmailForm(forms.Form):
	mensaje = forms.CharField(widget=forms.Textarea,label="Descripción breve",max_length=2000)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','email','first_name', 'last_name',)

class PermisoFormOrganizacion(forms.ModelForm):
	class Meta:
		model = Organizacion
		fields = ('nombre','usuario',)

class PedirPermisoForm(forms.Form):
	cual_org = forms.ModelChoiceField(queryset=Organizacion.objects.all(),
	                                           required=True,
	                                           label="Organización")
	asunto = forms.CharField( widget=forms.Textarea )


