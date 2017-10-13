# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from registration.backends.hmac.views import *

# Create your views here.
def index(request,template='index1.html'):
	object = Organizacion.objects.all()
	return render(request, template, locals())

def detail_org(request,template='detalle.html',slug=None):
	object = Organizacion.objects.get(slug=slug)
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