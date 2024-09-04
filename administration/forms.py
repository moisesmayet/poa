from django import forms
from django.forms import Form, ModelChoiceField, Select, TextInput

from authentication.models import CustomUser
from poa.models import Eje, Objetivo
from uapa.models import TipoEstamento, Estamento, Sede


class FormLinea(Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='linea')
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)

    linea_description = forms.CharField(label='Línea', widget=forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}))

    level1 = ModelChoiceField(label='Eje', empty_label=None, queryset=Eje.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))

    level2 = ModelChoiceField(label='Objetivo Estratégico', empty_label=None, queryset=Objetivo.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))


class FormEstamento(Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='estamento')
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)

    estamento_tipo = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=1)
    estamento_name = forms.CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    estamento_has_poa = forms.BooleanField(required=False, label='Tiene POA')

    estamento_sede = ModelChoiceField(empty_label=None, queryset=Sede.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))

    estamento_user = ModelChoiceField(empty_label=None, queryset=CustomUser.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))
