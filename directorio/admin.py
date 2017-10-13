# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Pais)
admin.site.register(TipoActividad)
admin.site.register(Participacion)
admin.site.register(ServiciosCadena)
admin.site.register(IntercambioTecnologia)

class ProductosServiciosInline(admin.TabularInline):
	model = ProductosServicios
	extra = 1

class OrganizacionAdmin(admin.ModelAdmin):
	inlines = [ProductosServiciosInline,]
	search_fields = ['nombre',]
	list_filter = ['pais_sede','tipo_organizacion']
	
	def get_form(self, request, obj=None, **kwargs):
		if not request.user.is_superuser:
			self.exclude = ('usuario',)
		return super(OrganizacionAdmin, self).get_form(request, obj=None, **kwargs)

	def get_queryset(self, request):
		if request.user.is_superuser:
			return Organizacion.objects.all()
		return Organizacion.objects.filter(usuario=request.user)

	def save_model(self, request, obj, form, change):
		if request.user.is_superuser:
			obj.save()
		else:
			obj.usuario = request.user
			obj.save() 

admin.site.register(Organizacion,OrganizacionAdmin)
