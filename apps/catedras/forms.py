#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Curso, CursoAlumno, Carrera, Materia
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import FilteredSelectMultiple, ForeignKeyRawIdWidget
from apps.aranceles.models import Arancel
from apps.entidades.models import Alumno
from django.core.exceptions import ValidationError
from datetime import datetime

class CursoForm(forms.ModelForm):
    #aranceles = forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple("Aranceles", is_stacked=False), queryset=Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=4))
    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/jsi18n',)
    class Meta:
        model = Curso
        exclude=[]
        widgets = {
            'carrera' : forms.Select(attrs = {'class':'form-control'}),            
            'inicio': SelectDateWidget(years=range(datetime.now().date().year - 5, datetime.now().date().year + 3, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'fin': SelectDateWidget(years=range(datetime.now().date().year - 5, datetime.now().date().year + 3, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'dias' : forms.CheckboxSelectMultiple(),
            'turno' : forms.TextInput(attrs = {'class':'form-control'}),
            'matricula' : forms.Select(attrs = {'class':'form-control'}),
            'matricula_fpo' : forms.Select(attrs = {'class':'form-control'}),
            'fecha_tope_matriculacion': SelectDateWidget(years=range(datetime.now().date().year - 5, datetime.now().date().year + 3, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'monto_cuota' : forms.Select(attrs = {'class':'form-control'}),            
            'cantidad_cuotas' : forms.TextInput(attrs = {'class':'form-control'}),
            'examen_ordinario' : forms.Select(attrs = {'class':'form-control'}),
            'examen_extra' : FilteredSelectMultiple("Aranceles", is_stacked=False, attrs = {'class':'form-control'}),
            'materias' : FilteredSelectMultiple("Materias", is_stacked=False, attrs = {'class':'form-control'}),
            'aranceles' : FilteredSelectMultiple("Aranceles", is_stacked=False, attrs = {'class':'form-control'}),
        }
    
    def clean(self):
        aranceles = self.cleaned_data.get('aranceles')
        carrera = self.cleaned_data.get('carrera')
        examen_extra = self.cleaned_data.get('examen_extra')
        if aranceles and carrera:
            for arancel in aranceles:
                if arancel.concepto.tipo_concepto.tipo_carrera.id != carrera.tipo.id:
                    raise ValidationError({'aranceles': u'Aranceles no se corresponden con el Tipo de carrera Seleccionado'})
        if examen_extra and carrera:
            for exa in examen_extra:
                if exa.concepto.tipo_concepto.tipo_carrera.id != carrera.tipo.id:
                    raise ValidationError({'examen_extra': u'Los Examenes no se corresponden con el Tipo de carrera Seleccionado'})

        return self.cleaned_data

    # def save(self, commit=True):
    #     instance = forms.ModelForm.save(self, False)
    #     materias = self.cleaned_data['materias']
    #     examen_extra = self.cleaned_data['examen_extra']
    #     aranceles = self.cleaned_data['aranceles']

    #     old_save_m2m = self.save_m2m
    #     def save_m2m():
    #         old_save_m2m()
    #         import pdb; pdb.set_trace()

    #         



from django.contrib.admin.sites import site
class CursoAlumnoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CursoAlumnoForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inscripcion'].initial = datetime.now()
    class Media:
        css = {'all': ('/static/admin/css/forms.css',),}
        js = ('/admin/jsi18n',)
    class Meta:
        model = CursoAlumno
        exclude = ['estado', 'observacion']
        widgets = {
            'curso' : forms.Select(attrs = {'class':'form-control'}),
            'alumno': ForeignKeyRawIdWidget(CursoAlumno._meta.get_field('alumno').rel, site),
            'fecha_inscripcion': SelectDateWidget(years=range(datetime.now().date().year - 1, datetime.now().date().year + 1, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
        }
    def clean(self):
        alumno = self.cleaned_data.get('alumno')
        curso = self.cleaned_data.get('curso')
        if alumno and curso:
            try: existe = CursoAlumno.objects.get(curso=curso, alumno=alumno)
            except: existe = False 
            if existe:
                raise ValidationError({'alumno': u'Este Alumno ya esta Inscripto en este curso'})
        return self.cleaned_data



class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        exclude = []
        widgets = {
            'tipo' : forms.Select(attrs = {'class':'form-control'}),
            'nombre' : forms.TextInput(attrs = {'class':'form-control',}),
            'grupo' : forms.Select(attrs = {'class':'form-control'}),
            'duracion' : forms.TextInput(attrs = {'class':'form-control',}),
        }


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        exclude = []
        widgets = {
            'nombre' : forms.TextInput(attrs = {'class':'form-control',}),
        }

