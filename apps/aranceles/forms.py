#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Concepto, Periodo, Arancel, TipoConcepto
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime
from django.core.exceptions import ValidationError


class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        exclude = []
        widgets = {
            'resolucion' : forms.TextInput(attrs = {'class':'form-control'}),
            'inicio': SelectDateWidget(years=range(datetime.now().date().year - 3, datetime.now().date().year + 3, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'fin': SelectDateWidget(years=range(datetime.now().date().year - 3, datetime.now().date().year + 3, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'estado': forms.Select(attrs = {'class':'form-control'}),
        }

class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        exclude = []
        widgets = {
            'tipo_concepto': forms.Select(attrs = {'class':'form-control'}),
            'concepto' : forms.TextInput(attrs = {'class':'form-control'}),
            'fraccionable_hasta' : forms.TextInput(attrs = {'class':'form-control'}),
            'funcion' : forms.TextInput(attrs = {'class':'form-control'}),
        }



class ArancelForm(forms.ModelForm):
    class Meta:
        model = Arancel
        exclude = []
        widgets = {
            'resolucion': forms.Select(attrs = {'class':'form-control'}),
            'concepto': forms.Select(attrs = {'class':'form-control'}),
            'monto' : forms.TextInput(attrs = {'class':'form-control'}),
        }

    def clean(self):
        resolucion = self.cleaned_data.get('resolucion')
        concepto = self.cleaned_data.get('concepto')

        if resolucion and concepto:
            if Arancel.objects.filter(concepto=concepto, resolucion=resolucion):
                raise ValidationError({'concepto': u'Ya existe un Arancel de %s en la Resolucion %s' % (concepto, resolucion) })
        return self.cleaned_data



class TipoConceptoForm(forms.ModelForm):
    class Meta:
        model = TipoConcepto
        exclude = []
        widgets = {
            'titulo' : forms.TextInput(attrs = {'class':'form-control'}),
        }



