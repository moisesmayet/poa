from django import forms
from django.forms import Form, ModelChoiceField, Select
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Eje, Objetivo, Linea, MedioVerificacion, Mes, Responsable


class FormPOA(Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='edit')
    name = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='poa')
    poa_id = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)
    poa_estamento = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)


class FormObjetivoOperativo(Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='edit')
    name = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='objetivo')
    poa_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    operativo_id = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)

    level1 = ModelChoiceField(label='Eje', empty_label=None, queryset=Eje.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))

    level2 = ModelChoiceField(label='Objetivo Estratégico', empty_label=None, queryset=Objetivo.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))

    level3 = ModelChoiceField(label='Línea de Actuación', empty_label=None, queryset=Linea.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))

    operativo_description = forms.CharField(label='Objetivo Operativo', widget=forms.Textarea(attrs={'rows': 3}))


class FormMeta(Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='edit')
    name = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='meta')
    operativo_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    meta_id = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)
    meta_description = forms.CharField(label='Meta', widget=forms.Textarea(attrs={'rows': 3}))


class FormActividad(Form):
    action = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='edit')
    name = forms.CharField(max_length=40, widget=forms.HiddenInput(), required=False, initial='actividad')
    meta_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    actividad_id = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)
    actividad_peso = forms.IntegerField(label='Peso', required=False, initial=100, min_value=1, max_value=100, validators=[MaxValueValidator(100), MinValueValidator(1)])
    actividad_description = forms.CharField(label='Actividad', widget=forms.Textarea(attrs={'rows': 3}))
    actividad_medio_nuevo = forms.CharField(label='Medio de Verificación (nuevo)', max_length=100, required=False)
    actividad_medio = ModelChoiceField(label='Medio de Verificación', empty_label=None, required=False, queryset=MedioVerificacion.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))
    actividad_responsable_nuevo = forms.CharField(label='Responsable (nuevo)', max_length=100, required=False)
    actividad_responsable = ModelChoiceField(label='Responsable', empty_label=None, required=False, queryset=Responsable.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))
    actividad_presupuesto = forms.DecimalField(required=False, label='Presupuesto', initial=0, min_value=0, validators=[MinValueValidator(0)])

    meses = Mes.objects.all()
    meses_choices = [(mes.id, "") for mes in meses]

    actividad_cronograma = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=meses_choices)


class FormCronograma(Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False, initial=0)
    cronograma_cumplimiento = forms.BooleanField(required=False, label='Actividad realizada')
