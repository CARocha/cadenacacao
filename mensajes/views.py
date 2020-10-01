# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Mensaje
from .forms import MensajeForm

# Create your views here.



def enviar_correo(request, template="correo.html"):
    if request.method == "POST":

        subject = request.POST.get("asunto")
        to_paises = request.POST.getlist("pais", None)
        to_tipo_organizacion = request.POST.getlist("tipo_organizacion", None)
        to_participacion_cadena = request.POST.getlist("participacion_cadena", None)
        to_organizacion = request.POST.getlist("organizacion")
        content = request.POST.get("contenido")
        form = MensajeForm(request.POST or None)
        if form.is_valid():
            print("###es valido####")
            #form.save()
            #luego que guarda envia correo para evidencia
            html_content = render_to_string("email/email.html",{'subject':subject,
                                                            'content':content})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                #subject,
                subject,
                #content,
                text_content,
                #from email,
                'simas@simas.org.ni',
                #settings.Email_HOST_USER,
                #los recipientes
                ['crocha09.09@gmail.com']
                )
            email.attach_alternative(html_content, "text/html")
            email.send()
            messages.success(request, "Se envio con exito el correo")
            return HttpResponseRedirect(reverse('mensajes:enviar_correo'))
    else:
        form = MensajeForm()

    return render(request, template, locals())