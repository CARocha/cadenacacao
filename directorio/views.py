# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Q
from registration.backends.hmac.views import *

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
		params['tipo_organizacion'] = request.session['tipo_organizacion']

	if request.session['paises_labora']:
		params['paises_labora__in'] = request.session['paises_labora']

	if request.session['participacion_cadena']:
		params['participacion_cadena__in'] = request.session['participacion_cadena']

	if request.session['servicios']:
		params['servicios__in'] = request.session['servicios']

	if request.session['intercambio']:
		params['intercambio__in'] = request.session['intercambio']

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

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1

			# return HttpResponseRedirect('/afiliados/datos-personales/')
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
		except:
			pass

	if request.GET.get('q'):
		search_text = request.GET['q']
		if search_text is not None and search_text != u'':
			object_list = Organizacion.objects.filter(Q(nombre__icontains=search_text)).distinct().order_by('nombre')
	elif 'pais_sede' not in request.session:
		object_list = Organizacion.objects.all().order_by('nombre')
	else:
		filtro = _queryset_filtrado_afiliado(request)
		object_list = filtro

	return render(request, template, locals())

def detail_org(request,template='perfil.html',slug=None):
	object = Organizacion.objects.get(slug=slug)
	fotos = ProductosServicios.objects.filter(organizacion = object)
	conteo = fotos.count() / 3

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