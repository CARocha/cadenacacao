# -*- coding: UTF-8 -*-
from .models import SiteConfiguration
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ConfiguracionForm(forms.ModelForm):
    acerca_footer = forms.CharField(label='Texto pie de pagina',max_length=3000,widget=CKEditorUploadingWidget)
    politica_condicines = forms.CharField(label='Politicas y condiciones',max_length=5000,widget=CKEditorUploadingWidget)

    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        exclude = ['acerca']
