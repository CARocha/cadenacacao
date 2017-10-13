# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from directorio.models import *
from directorio.forms import *
from django.db.models import Q

def buscador(request):
	form = BuscadorForm()
	if request.method == 'GET':
		search_text = request.GET['q']
		resultados = Organizacion.objects.filter(Q(nombre__icontains=search_text)).distinct()
		print resultados
	else:
		resultados = []

	return render(request, 'index.html',{'form':form,'resultados':resultados})