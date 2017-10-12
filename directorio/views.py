# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *

# Create your views here.
def index(request,template='index1.html'):
	object = Organizacion.objects.all()
	return render(request, template, locals())

def detail_org(request,template='detalle.html',slug=None):
	object = Organizacion.objects.get(slug=slug)
	return render(request, template, locals())
