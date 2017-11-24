# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Q
from registration.backends.hmac.views import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, EmailMultiAlternatives
import json as simplejson
from django.forms import inlineformset_factory
from django.contrib.postgres.search import SearchVector

# Create your views here.
def index(request,template='index.html'):
	# object = Organizacion.objects.all()
	return render(request, template, locals())

def _queryset_filtrado_afiliado(request):
	params = {}

	if request.session['pais_sede']:
		params['pais_sede'] = request.session['pais_sede']

	if request.session['ambito_accion']:
		params['ambito_accion'] = request.session['ambito_accion']

	if request.session['tipo_organizacion']:
		params['tipo_organizacion__in'] = request.session['tipo_organizacion']

	if request.session['paises_labora']:
		params['paises_labora__in'] = request.session['paises_labora']

	if request.session['participacion_cadena']:
		params['participacion_cadena__in'] = request.session['participacion_cadena']

	if request.session['servicios']:
		params['servicios__in'] = request.session['servicios']

	if request.session['intercambio']:
		params['intercambio__in'] = request.session['intercambio']

	# if request.session['tipo']:
	# 	params['tipo'] = request.session['tipo']

	if request.session['tipo_actividad']:
		params['tipo_actividad__in'] = request.session['tipo_actividad']

	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	return Organizacion.objects.filter(**params).order_by('nombre')

def consulta(request,template='consulta.html'):
	if request.method == 'POST':
		mensaje = None
		form = OrganizacionForm(request.POST)
		if form.is_valid():
			request.session['pais_sede'] = form.cleaned_data['pais_sede']
			request.session['ambito_accion'] = form.cleaned_data['ambito_accion']
			request.session['tipo_organizacion'] = form.cleaned_data['tipo_organizacion']
			request.session['paises_labora'] = form.cleaned_data['paises_labora']
			request.session['participacion_cadena'] = form.cleaned_data['participacion_cadena']
			request.session['servicios'] = form.cleaned_data['servicios']
			request.session['intercambio'] = form.cleaned_data['intercambio']
			# request.session['tipo'] = form.cleaned_data['tipo']
			request.session['tipo_actividad'] = form.cleaned_data['tipo_actividad']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1

		else:
			centinela = 0

	else:
		form = OrganizacionForm()
		mensaje = "Existen alguno errores"
		try:
			del request.session['pais_sede']
			del request.session['ambito_accion']
			del request.session['tipo_organizacion']
			del request.session['paises_labora']
			del request.session['participacion_cadena']
			del request.session['servicios']
			del request.session['intercambio']
			# del request.session['tipo']
			del request.session['tipo_actividad']
		except:
			pass

	if request.GET.get('q'):
		search_text = request.GET['q']
		if search_text is not None and search_text != u'':
			object_list = Organizacion.objects.filter(Q(nombre__icontains=search_text)|
													Q(pais_sede__nombre__icontains=search_text)|
													Q(tipo_organizacion__icontains=search_text)|
													Q(contacto_1__icontains=search_text)|
													Q(contacto_2__icontains=search_text)|
													Q(tipo_actividad__nombre__icontains=search_text)|
													Q(participacion_cadena__nombre__icontains=search_text)|
													Q(servicios__nombre__icontains=search_text)|
													Q(ambito_accion__icontains=search_text)|
													Q(paises_labora__nombre__icontains=search_text)|
													Q(cobertura__icontains=search_text)|
													Q(intercambio__nombre__icontains=search_text)
													).distinct().order_by('nombre')

			# object_list = Organizacion.objects.annotate(search=SearchVector('nombre','objetivo','pais_sede__nombre',
			# 											'tipo_organizacion','tipo_actividad__nombre',
			# 											'participacion_cadena__nombre','servicios__nombre',
			# 											'ambito_accion','paises_labora__nombre',
			# 											'cobertura','intercambio__nombre')).filter(search=search_text).order_by('nombre').distinct()

	elif 'pais_sede' not in request.session:
		object_list = Organizacion.objects.all().order_by('nombre')
	else:
		filtro = _queryset_filtrado_afiliado(request)
		object_list = filtro

	return render(request, template, locals())

def detail_org(request,template='perfil.html',slug=None):
	object = Organizacion.objects.get(slug=slug)
	fotos = ProductosServicios.objects.filter(organizacion = object)
	conteo = fotos.count()

	location = object.location.split(",")

	return render(request, template, locals())

class MyRegistrationView(RegistrationView):
	def create_inactive_user(self, form):
		"""
		Create the inactive user account and send an email containing
		activation instructions.

		"""
		new_user = form.save(commit=False)
		new_user.is_active = False
		new_user.is_staff = True
		new_user.save()

		self.send_activation_email(new_user)

		return new_user

@login_required
def user_profile(request,template='perfil_user.html'):
	user = User.objects.get(username = request.user)
	organizaciones = Organizacion.objects.filter(usuario = user)

	if request.method == 'POST':
		form = EmailForm(request.POST)
		if form.is_valid():
			mensaje = form.cleaned_data['mensaje']
		try:
			subject, from_email = 'Solicitud ingreso de organización o especialista a Sistema Cadena de cacao', 'noreply@unag-datos.org'
			text_content = 'Usuario: ' + str(user.username) + '<br>'  + \
							'Correo: ' + str(user.email) + '<br>'  + \
							'Mensaje: ' + str(mensaje)

			html_content = 'Usuario: ' + str(user.username) + '<br>'  + \
							'Correo: ' + str(user.email) + '<br>'  + \
							'Mensaje: ' + str(mensaje)

			msg = EmailMultiAlternatives(subject, text_content, from_email, ['cadenacacao@gmail.com',])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

			enviado = 1
			form = EmailForm()
		except:
			pass

	else:
		form = EmailForm()

	return render(request, template, locals())

@login_required
def editar_user(request,template='editar_user.html'):
	if request.method == 'POST':
		form = UserForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/profile/')
	else:
		form = UserForm(instance=request.user)

	return render(request, template, locals())

from django.contrib.auth.views import password_reset

@login_required
def editar_org(request,template='editar_org.html',slug=None):
	object = Organizacion.objects.get(slug=slug)
	FormSetInit = inlineformset_factory(Organizacion, ProductosServicios, form=ProductosServiciosFrom,max_num=9,extra=9)

	if request.method == 'POST':
		form = OrgForm(request.POST, instance=object)
		formset = FormSetInit(request.POST,request.FILES,instance=object)
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return HttpResponseRedirect('/accounts/profile/')

	else:
		form = OrgForm(instance=object)
		formset = FormSetInit(instance=object)

	return render(request, template, locals())

def obtener_lista(request):
	if request.is_ajax():
		lista = []
		for objeto in Organizacion.objects.all():
			split_location = objeto.location.split(",")
			dicc = dict(nombre=objeto.nombre ,id=objeto.id,
						lat=float(split_location[0]),
						lon=float(split_location[1])
						)
			lista.append(dicc)

		serializado = simplejson.dumps(lista)
		return HttpResponse(serializado, content_type = 'application/json')