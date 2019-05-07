# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import password_reset
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.forms import inlineformset_factory
from registration.backends.hmac.views import *

from .models import *
from .forms import *

import json as simplejson
# from django.contrib.postgres.search import SearchVector

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

	# if request.session['intercambio']:
	# 	params['intercambio__in'] = request.session['intercambio']

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
			# request.session['intercambio'] = form.cleaned_data['intercambio']
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
			# del request.session['intercambio']
			# del request.session['tipo']
			del request.session['tipo_actividad']
		except:
			pass

	if 'pais_sede' not in request.session:
		object_list = Organizacion.objects.all().order_by('-ratings__average','nombre')
	else:
		filtro = _queryset_filtrado_afiliado(request)
		object_list = filtro.order_by('-ratings__average','nombre')

	return render(request, template, locals())

def detail_org(request,template='perfil.html',slug=None):
	object = Organizacion.objects.get(slug=slug)
	fotos = ProductosServicios.objects.filter(organizacion = object)
	conteo = fotos.count()

	redes = Redes.objects.filter(organizacion = object).order_by('id')

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


	# if request.method == 'POST':
	# 	form = EmailForm(request.POST)
	# 	if form.is_valid():
	# 		mensaje = form.cleaned_data['mensaje']
	# 	try:
	# 		subject, from_email = 'Solicitud ingreso de organización o especialista a Sistema Cadena de cacao', 'vecomesoamerica@gmail.com'
	# 		text_content = 'Usuario: ' + str(user.username) + '<br>'  + \
	# 						'Correo: ' + str(user.email) + '<br>'  + \
	# 						'Mensaje: ' + str(mensaje)

	# 		html_content = 'Usuario: ' + str(user.username) + '<br>'  + \
	# 						'Correo: ' + str(user.email) + '<br>'  + \
	# 						'Mensaje: ' + str(mensaje)

	# 		msg = EmailMultiAlternatives(subject, text_content, from_email, ['cadenacacao@gmail.com','vecomesoamerica@gmail.com','guisselle.aleman@rikolto.org','selene.casanova@rikolto.org'])
	# 		msg.attach_alternative(html_content, "text/html")
	# 		msg.send()

	# 		enviado = 1
	# 		form = EmailForm()
	# 	except:
	# 		pass

	# else:
	# 	form = EmailForm()

	if request.method == 'POST':
		form1 = PedirPermisoForm(request.POST)
		if form1.is_valid():
			org_slug = form1.cleaned_data['cual_org'].id
			orga = get_object_or_404(Organizacion, pk=org_slug)
			mensaje = form1.cleaned_data['asunto']
		try:
			subject, from_email = 'Solicitud ingreso de organización o especialista a Sistema Cadena de cacao', 'vecomesoamerica@gmail.com'
			text_content = 'Usuario: ' + str(user.username) + '<br>'  + \
							'Correo: ' + str(user.email) + '<br>'  + \
							'Mensaje: ' + str(mensaje)

			html_content = 'Usuario: ' + str(user.username) + '<br>'  + \
							'Correo: ' + str(user.email) + '<br>'  + \
							'Mensaje: ' + str(mensaje)

			msg = EmailMultiAlternatives(subject, text_content, from_email,
			                             [obj.email for obj in orga.usuario.all()])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

			enviado = 1
			form1 = PedirPermisoForm()
		except:
			pass

	else:
		form1 = PedirPermisoForm()

	return render(request, template, locals())

@login_required
def permisos_organizacion(request,template='editar_permisos.html',slug=None):
	org = get_object_or_404(Organizacion, slug=slug)
	if request.method == 'POST':
		form = PermisoFormOrganizacion(request.POST,request.FILES,instance=org)
		if form.is_valid():
			form.save()
			obj = form.save(commit=False)
			obj.usuario.add(request.user)
			obj.save()
			mandar_aviso(request,org)
			return HttpResponseRedirect('/accounts/profile/')

	else:
		form = PermisoFormOrganizacion(instance=org)
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



@login_required
def crear_org(request,template='crear_org.html'):
	FormSetInit = inlineformset_factory(Organizacion, ProductosServicios,
	                                    form=ProductosServiciosFrom,
	                                    max_num=9,extra=9)
	FormSetInit2 = inlineformset_factory(Organizacion, Redes,
	                                     form=RedesFrom,
	                                     extra=11,max_num=11)

	if request.method == 'POST':
		form = OrgForm(request.POST,request.FILES)
		formset = FormSetInit(request.POST,request.FILES)
		formset2 = FormSetInit2(request.POST,request.FILES)

		if form.is_valid() and formset.is_valid() and formset2.is_valid():
			form.save()
			org = form.save(commit=False)
			org.usuario.add(request.user)
			org.save()
			#guarda formsets inlines
			formset.save()
			formset2.save()
			return HttpResponseRedirect('/accounts/profile/')

	else:
		form = OrgForm()
		formset = FormSetInit()
		formset2 = FormSetInit2()

	return render(request, template, locals())


@login_required
def editar_org(request,template='editar_org.html',slug=None):
	object = Organizacion.objects.get(slug=slug)
	FormSetInit = inlineformset_factory(Organizacion, ProductosServicios, form=ProductosServiciosFrom,max_num=9,extra=9)
	FormSetInit2 = inlineformset_factory(Organizacion, Redes, form=RedesFrom,extra=11,max_num=11)

	if request.method == 'POST':
		form = OrgForm(request.POST,request.FILES,instance=object)
		formset = FormSetInit(request.POST,request.FILES,instance=object)
		formset2 = FormSetInit2(request.POST,request.FILES,instance=object)
		if form.is_valid() and formset.is_valid() and formset2.is_valid():
			form.save()
			formset.save()
			formset2.save()
			return HttpResponseRedirect('/accounts/profile/')

	else:
		form = OrgForm(instance=object)
		formset = FormSetInit(instance=object)
		formset2 = FormSetInit2(instance=object)

	return render(request, template, locals())

def obtener_lista(request):
	if request.is_ajax():
		lista = []
		for objeto in Organizacion.objects.all():
			if objeto.location:
				split_location = objeto.location.split(",")
				dicc = dict(nombre=objeto.nombre ,id=objeto.id,
							lat=float(split_location[0]),
							lon=float(split_location[1])
							)
				lista.append(dicc)

		serializado = simplejson.dumps(lista)
		return HttpResponse(serializado, content_type = 'application/json')

def mandar_aviso(request, org=None):
	user = User.objects.get(username = request.user)
	orga = get_object_or_404(Organizacion, pk=org.id)

	subject, from_email = 'Permiso otorgado!!', 'vecomesoamerica@gmail.com'
	text_content = 'Usuario: ' + str(user.username) + '<br>'  + \
					'Correo: ' + str(user.email) + '<br>'  + \
					'Mensaje: ' + 'Ha otorgado permiso!'

	html_content = 'Usuario: ' + str(user.username) + '<br>'  + \
					'Correo: ' + str(user.email) + '<br>'  + \
					'Mensaje: ' + 'Ha otorgado permiso!'

	msg = EmailMultiAlternatives(subject, text_content, from_email,
	                             [obj.email for obj in orga.usuario.all()])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

	return 1
