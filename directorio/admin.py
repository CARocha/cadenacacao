# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from django.core.mail import send_mail, EmailMultiAlternatives
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class PaisAdmin(ImportExportModelAdmin):
	pass

class TipoActividadAdmin(ImportExportModelAdmin):
	pass

class ParticipacionAdmin(ImportExportModelAdmin):
	pass

class ServiciosCadenaAdmin(ImportExportModelAdmin):
	pass

class IntercambioTecnologiaAdmin(ImportExportModelAdmin):
	pass

admin.site.register(Pais,PaisAdmin)
admin.site.register(TipoActividad,TipoActividadAdmin)
admin.site.register(Participacion,ParticipacionAdmin)
admin.site.register(ServiciosCadena,ServiciosCadenaAdmin)
admin.site.register(IntercambioTecnologia,IntercambioTecnologiaAdmin)

class ProductosServiciosInline(admin.TabularInline):
	model = ProductosServicios
	extra = 1
	max_num = 9

class OrganizacionAdmin(ImportExportModelAdmin):
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

		if obj.usuario:
			print obj.usuario.email
			try:
				subject, from_email = 'Perfil activo en Sistema Cadena de cacao', 'noreply@unag-datos.org'
				text_content = 'Se ha asignado la Organizacion/Especialista ' + str(obj.nombre) +  'usuario ' + str(obj.usuario) 

				html_content = 'Se ha asignado el usuario ' + str(obj.usuario)

				msg = EmailMultiAlternatives(subject, text_content, from_email, [obj.usuario.email,])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
			except:
				pass

admin.site.register(Organizacion,OrganizacionAdmin)
