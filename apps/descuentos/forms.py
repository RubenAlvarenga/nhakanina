#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Descuento
from django.core.exceptions import ValidationError
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime, date
from django.contrib.admin.widgets import FilteredSelectMultiple, ForeignKeyRawIdWidget
from django.contrib.admin.sites import site

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        exclude=[]
        widgets = {
            'motivo' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Motivo' }),
            'cant_minima_concepto' : forms.TextInput(attrs = {'class':'form-control'}),
            'cant_maxima_concepto' : forms.TextInput(attrs = {'class':'form-control'}),
            'porcentaje' : forms.TextInput(attrs = {'class':'form-control'}),
            'tipo_carrera_concepto' : forms.Select(attrs = {'class':'form-control'}),
            'funcion' : forms.Select(attrs = {'class':'form-control' }),

        }
