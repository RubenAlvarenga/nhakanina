#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Persona, Alumno
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets
from datetime import datetime

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = []
        widgets = {
            'cedula' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Nro de Cédula de Identidad' }),
            'nombre1' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Nombre' }),
            'nombre2' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Segundo Nombre' }),
            'apellido1' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Apellido' }),
            'apellido2' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Segundo Apellido' }),
            'nacionalidad' : forms.Select(attrs = {'class':'form-control'}),
            'fecha_nacimiento' : SelectDateWidget(years=range(1930, datetime.now().date().year + 1, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}), 
        }
    def clean_cedula(self):
        return self.cleaned_data['cedula'].strip()
    def clean_nombre1(self):
        return self.cleaned_data['nombre1'].strip().capitalize()
    def clean_nombre2(self):
        return self.cleaned_data['nombre2'].strip().capitalize()
    def clean_apellido1(self):
        return self.cleaned_data['apellido1'].strip().capitalize()
    def clean_apellido2(self):
        return self.cleaned_data['apellido2'].strip().capitalize()


class AlumnoForm(PersonaForm):
    class Meta:
        model = Alumno
        exclude = []
        widgets = {
            'cedula' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Nro de Cédula de Identidad' }),
            'nombre1' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Nombre' }),
            'nombre2' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Segundo Nombre' }),
            'apellido1' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Apellido' }),
            'apellido2' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Segundo Apellido' }),
            'nacionalidad' : forms.Select(attrs = {'class':'form-control'}),
            'fecha_nacimiento' : SelectDateWidget(years=range(1930, datetime.now().date().year + 1, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}), 
        }
    def clean_cedula(self):
        return self.cleaned_data['cedula'].strip()
    def clean_nombre1(self):
        return self.cleaned_data['nombre1'].strip().capitalize()
    def clean_nombre2(self):
        return self.cleaned_data['nombre2'].strip().capitalize()
    def clean_apellido1(self):
        return self.cleaned_data['apellido1'].strip().capitalize()
    def clean_apellido2(self):
        return self.cleaned_data['apellido2'].strip().capitalize()

# class empresaForm(forms.ModelForm):
#     class Meta:
#         model = empresa
#         exclude = []
#         widgets = {
#             'nombrereal' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese El Nombre Real (p/Facturacion)' }),
#             'nombrefantasia' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Nombre Fantasia' }),
#         }

# class clientePersonaForm(personaForm):
#     ruc= forms.CharField(label='RUC',max_length=10, required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
#     def __init__(self, *args, **kwargs):
#         super(personaForm, self).__init__(*args,**kwargs)
#     class Meta:
#         model = persona
#         fields = ['ruc', 'cedula', 'nombre1', 'nombre2', 'apellido1', 'apellido2']
#         widgets = {
#             'cedula' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Nro de Cédula de Identidad' }),
#             'nombre1' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Nombre' }),
#             'nombre2' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Segundo Nombre' }),
#             'apellido1' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Apellido' }),
#             'apellido2' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese Segundo Apellido' }),
#         }


# class clienteEmpresaForm(empresaForm):
#     ruc= forms.CharField(label='RUC',max_length=10, required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))
#     def __init__(self, *args, **kwargs):
#         super(empresaForm, self).__init__(*args,**kwargs)
#     class Meta:
#         model = empresa
#         fields = ['ruc', 'nombrereal', 'nombrefantasia']
#         widgets = {
#             'nombrereal' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Ingrese El Nombre Real (p/Facturacion)' }),
#             'nombrefantasia' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Ingrese Nombre Fantasia' }),
#         }


# # class selectTipoClienteForm(forms.Form):
# #     CHOICES = (('1', 'Persona',), ('2', 'Empresa',))
# #     like = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)
