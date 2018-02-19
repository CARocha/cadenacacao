# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from django.core.mail import send_mail, EmailMultiAlternatives
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets

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

class RedesInline(admin.TabularInline):
	model = Redes
	extra = 1

class OrganizacionResource(resources.ModelResource):
	class Meta:
		model = Organizacion
		fields = ('id','nombre','logo','objetivo','contacto_1','correo_1','telefono_1','contacto_2',
					'correo_2','telefono_2','pais_sede','ciudad','location','tipo_organizacion',
					'tipo_actividad','participacion_cadena','servicios','ambito_accion',
					'paises_labora','cobertura','periodo_permanencia','intercambio','sitio_web',
					'miembros','tamano','actualizado','slug','ratings','usuario')

	def dehydrate_pais_sede(self, org):
		return '%s' % (org.pais_sede.nombre)

	def dehydrate_tipo_actividad(self, org):
		return '%s' % (",".join([p.nombre for p in org.tipo_actividad.all()]))

	def dehydrate_participacion_cadena(self, org):
		return '%s' % (",".join([p.nombre for p in org.participacion_cadena.all()]))

	def dehydrate_servicios(self, org):
		return '%s' % (",".join([p.nombre for p in org.servicios.all()]))

	def dehydrate_paises_labora(self, org):
		return '%s' % (",".join([p.nombre for p in org.paises_labora.all()]))

	def dehydrate_intercambio(self, org):
		return '%s' % (",".join([p.nombre for p in org.intercambio.all()]))

class OrganizacionAdmin(ImportExportModelAdmin):
	inlines = [RedesInline,ProductosServiciosInline]
	search_fields = ['nombre','objetivo','pais_sede__nombre','paises_labora__nombre']
	list_filter = ['pais_sede','tipo_organizacion']
	resource_class = OrganizacionResource
	
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
				subject, from_email = 'Perfil activo en Sistema Cadena de cacao', 'vecomesoamerica@gmail.com'
				text_content = 'Se ha asignado al usuario ' + str(obj.usuario) + 'la Organizacion/Especialista' + str(obj.nombre) + \
								'Diríjase a la siguiente direccion: directoriocacao.info/accounts/profile/'

				html_content = 'Se ha asignado al usuario ' + str(obj.usuario) + 'la Organizacion/Especialista' + str(obj.nombre) + \
								'Diríjase a la siguiente direccion: directoriocacao.info/accounts/profile/'

				msg = EmailMultiAlternatives(subject, text_content, from_email, [obj.usuario.email,])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
			except:
				pass

admin.site.register(Organizacion,OrganizacionAdmin)
