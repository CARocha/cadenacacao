from django import forms
from directorio.models import Organizacion, Participacion, TIPO_CHOICES, Pais
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


def paises():
    foo = Organizacion.objects.order_by('pais_sede').distinct().values_list('pais_sede__id', flat=True)
    return Pais.objects.filter(id__in=foo)

class MensajeForm(forms.ModelForm):
    pais = forms.ModelMultipleChoiceField(queryset=Pais.objects.all(),
            required=False,  widget=forms.SelectMultiple(attrs={"class":"prueba form-control"}))
    tipo_organizacion = forms.ChoiceField(choices=TIPO_CHOICES,
                                        required=False,  widget=forms.Select(attrs={"class":"prueba form-control"}))
    participacion_cadena = forms.ModelMultipleChoiceField(queryset=Participacion.objects.all(),
                                            required=False,  widget=forms.SelectMultiple(attrs={"class":"prueba form-control"}))
    destinatario = forms.ModelMultipleChoiceField(queryset=Organizacion.objects.all(),
                                    required=False, widget=forms.SelectMultiple(attrs={"class":"prueba form-control"}))
    asunto = forms.CharField( widget=forms.TextInput(attrs={"class":"prueba form-control"}))
    contenido = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":40,"class":"prueba form-control"}))
    class Meta:
        model=Mensaje
        fields = ('pais', 'tipo_organizacion', 
                  'participacion_cadena', 'destinatario',
                  'asunto', 'contenido')
    # def __init__(self, *args, **kwargs):
    #     super(MensajeForm, self).__init__(*args, **kwargs)
    #     self.fields['pais'] = forms.ModelChoiceField(queryset=Pais.objects.all(),
    #                                 required=False, widget=forms.SelectMultiple(attrs={"class":"prueba form-control"}))
    #     self.fields['tipo_organizacion'] = forms.MultipleChoiceField(choices=TIPO_CHOICES,
    #                                         required=False,  widget=forms.SelectMultiple(attrs={"class":"prueba form-control"}))
    #     self.fields['participacion_cadena'] = forms.ModelMultipleChoiceField(queryset=Participacion.objects.all(),
    #                                             required=False,  widget=forms.SelectMultiple(attrs={"class":"prueba form-control"}))
    #     self.fields['organizacion'] = forms.ModelMultipleChoiceField(queryset=Organizacion.objects.all(),
    #                                     required=False, widget=forms.SelectMultiple(attrs={"class":"prueba form-control"}))
    #     self.fields['asunto'] = forms.CharField( widget=forms.TextInput(attrs={"class":"prueba form-control"}))
    #     self.fields['contenido'] = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":40,"class":"prueba form-control"}))





