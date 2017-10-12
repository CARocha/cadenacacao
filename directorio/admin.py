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

admin.site.register(Organizacion,OrganizacionAdmin)
