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
from directorio.models import Organizacion
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def enviar_correo(request, template="correo.html"):
    if request.method == "POST":

        subject = request.POST.get("asunto")
        to_paises = request.POST.getlist("pais")
        to_tipo_organizacion = request.POST.get("tipo_organizacion")
        to_participacion_cadena = request.POST.getlist("participacion_cadena")
        to_organizacion = request.POST.getlist("destinatario")        
        content = request.POST.get("contenido")
        data = {}
        if to_paises != []:
            data['pais_sede_id__in'] = to_paises
        if to_tipo_organizacion != '':
            data['tipo_organizacion__exact'] = to_tipo_organizacion
        if to_participacion_cadena != []:
            data['participacion_cadena__in'] = to_participacion_cadena
        if to_organizacion != []:
            data['id__in'] = to_organizacion
        #print(data) 
        filtro = Organizacion.objects.filter(**data)
        lista_destinos = []
        for obj in filtro:
            if obj.correo_1 != None and obj.correo_1 != '':
                lista_destinos.append(obj.correo_1)
            if obj.correo_2 != None and obj.correo_2 != '':
                lista_destinos.append(obj.correo_2)
            for mail in obj.usuario.all():
                if mail.email != None:
                    lista_destinos.append(mail.email)
       
        correos_destinos = [i for i in lista_destinos if ('@' in i)]
        
        form = MensajeForm(request.POST or None)
        if form.is_valid():
            #print("###es valido####")
            instance = form.save(commit=False)
            instance.usuario = request.user
            instance.save()
            form.save_m2m()
            
            #luego que guarda envia correo para evidencia
            html_content = render_to_string("email/email.html",{'subject':subject,
                                                            'content':content,
                                                            'user': request.user})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject,
                text_content,
                'simas@simas.org.ni',
                #settings.Email_HOST_USER,
                correos_destinos,
                reply_to=[request.user.email]
                )
            email.attach_alternative(html_content, "text/html")
            email.send()
            messages.success(request, "Se envio con exito el correo")
            return HttpResponseRedirect(reverse('mensajes:enviar_correo'))
    else:
        form = MensajeForm()

    return render(request, template, locals())