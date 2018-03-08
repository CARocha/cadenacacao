# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from django.core.mail import send_mail, EmailMultiAlternatives
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets
from .forms import *

from django.contrib.flatpages.models import FlatPage
# Note: we are renaming the original Admin and Form as we import them!
#flatpages admin ckeditor start ----------------------------------------------
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.forms import FlatpageForm as FlatpageFormOld

from ckeditor_uploader.widgets import CKEditorUploadingWidget
 
class FlatpageForm(FlatpageFormOld):
	content = forms.CharField(widget=CKEditorUploadingWidget(),required=False)
	class Meta:
		model = FlatPage # this is not automatically inherited from FlatpageFormOld
		fields = '__all__'
 
class FlatPageAdmin(FlatPageAdminOld):
	form = FlatpageForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
#flatpages admin ckeditor end-----------------------------------------------------

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

# cambiar str user en el admin
class CustomModelChoiceField(forms.ModelMultipleChoiceField):
	 def label_from_instance(self, obj):
	 	if obj.first_name or obj.last_name:
	 		return "%s %s / %s" % (obj.first_name, obj.last_name, obj.username)
	 	else:
	 		return obj.username

class MyInvoiceAdminForm(forms.ModelForm):
	usuario = CustomModelChoiceField(queryset=User.objects.all(),required=False) 
	class Meta:
		  model = Organizacion
		  fields = ('__all__')
######

class OrganizacionAdmin(ImportExportModelAdmin):
	inlines = [RedesInline,ProductosServiciosInline]
	search_fields = ['nombre','objetivo','pais_sede__nombre','paises_labora__nombre']
	list_filter = ['pais_sede','tipo_organizacion']
	resource_class = OrganizacionResource
	exclude = ['sitio_web',]
	form = MyInvoiceAdminForm
	
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
			for x in obj.usuario.all():
				try:
					subject, from_email = 'Perfil activo en Sistema Cadena de cacao', 'vecomesoamerica@gmail.com'
					text_content = 'Se ha asignado una Organización/Especialista al usuario ' + str(x.username) + '<br>' \
									'Ir a la dirección www.directoriocacao.info/accounts/profile/'

					html_content = 'Se ha asignado una Organización/Especialista al usuario ' + str(x.username) + '<br>' \
									'Ir a la dirección www.directoriocacao.info/accounts/profile/' 

					msg = EmailMultiAlternatives(subject, text_content, from_email, [x.email,])
					msg.attach_alternative(html_content, "text/html")
					msg.send()
				except Exception as e:
					print e

	class Media:
		css = {
			'all': ('css/select2.min.css',)
		}
		js = ('js/jquery-1.11.3.min.js','js/select2.min.js','js/admin.js',)


admin.site.register(Organizacion,OrganizacionAdmin)
