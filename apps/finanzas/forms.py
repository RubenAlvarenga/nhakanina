#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from apps.finanzas.models import PlanPago, ReciboPlanPago, Recibo
from django.core.exceptions import ValidationError
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime, date
from django.contrib.admin.widgets import FilteredSelectMultiple, ForeignKeyRawIdWidget
from apps.entidades.models import Persona
from django.contrib.admin.sites import site

class PlanPagoForm(forms.ModelForm):
    class Media:
        css = {'all': ('/static/admin/css/forms.css',),}
        js = ('/admin/jsi18n',)
    class Meta:
        model = PlanPago
        exclude=['secuencia', 'monto', 'estado', 'total_cuotas']
        widgets = {
            'vencimiento': SelectDateWidget(years=range(datetime.now().date().year, datetime.now().date().year + 3, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'curso_alumno' : ForeignKeyRawIdWidget(PlanPago._meta.get_field('curso_alumno').rel, site),
            'cantidad' : forms.TextInput(attrs = {'class':'form-control'}),
            'concepto' : ForeignKeyRawIdWidget(PlanPago._meta.get_field('concepto').rel, site),            
            'materia' : forms.Select(attrs = {'class':'form-control'}),
            'observaciones' : forms.Textarea(attrs = { 'class':'form-control'} ),
        }


class updPlanPagoForm(forms.ModelForm):
    class Meta:
        model = PlanPago
        exclude=['secuencia', 'monto', 'estado', 'total_cuotas']
        widgets = {
            'vencimiento': SelectDateWidget(years=range(datetime.now().date().year, datetime.now().date().year + 3, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'curso_alumno' : forms.Select(attrs = {'class':'form-control'}),
            'cantidad' : forms.TextInput(attrs = {'class':'form-control'}),
            'concepto' : forms.Select(attrs = {'class':'form-control'}),
            'materia' : forms.Select(attrs = {'class':'form-control'}),
            'observaciones' : forms.Textarea(attrs = { 'class':'form-control'} ),
        }

    

class ReciboPlanPagoForm(forms.ModelForm):
    class Meta:
        model = ReciboPlanPago
        exclude = ['concepto', 'monto', 'cantidad', 'estado', 'observaciones']
        widgets = {
            'fecha': SelectDateWidget(years=range(1900, datetime.now().date().year + 1, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'serie' : forms.TextInput(attrs = {'class':'form-control',}),
            'nro_recibo' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Verifique nro de recibo', 'autofocus' : 'autofocus', 'autocomplete' : 'off' }),
            'persona' : forms.Select(attrs = {'class':'form-control'}),
            'plan_pago' : forms.CheckboxSelectMultiple(),
        }


    def __init__(self, *args, **kwargs):
        super(ReciboPlanPagoForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial = datetime.now()

    def clean(self):
        plan_pago = self.cleaned_data.get('plan_pago')
        persona = self.cleaned_data.get('persona')
        nro_recibo = self.cleaned_data.get('nro_recibo')
        serie = self.cleaned_data.get('serie')
        descuentos = self.cleaned_data.get('descuentos')
        
        if descuentos and plan_pago:
            for desc in descuentos:
                if desc.tipo_carrera_concepto != plan_pago[0].concepto.concepto.tipo_concepto:
                    raise ValidationError({'descuentos': u'Este descuento no es aplicable a este concepto' })
                if desc.cant_minima_concepto > len(plan_pago) or desc.cant_maxima_concepto < len(plan_pago):
                    raise ValidationError({'descuentos': u'para aplicar %s es necesario un minimo de %s y un maximo de %s planes' % (desc.motivo, desc.cant_minima_concepto, desc.cant_maxima_concepto) })


        if nro_recibo and serie:
            if Recibo.objects.filter(nro_recibo=nro_recibo, serie=serie):
                raise ValidationError({'nro_recibo': u'Ya existe un Recibo con el numero: %s de la serie: %s' % (str(nro_recibo), serie) })
        if persona and plan_pago:
            concepto=[]
            for plan in plan_pago:
                concepto.append(plan.concepto.concepto)
                if plan.curso_alumno.alumno.cedula != persona.cedula:
                    raise ValidationError({'plan_pago': u'Los pagos no se corresponden al Alumno Seleccionado: '+str(persona) })
            if concepto:
                if len(set(concepto)) > 1:
                    raise ValidationError({'plan_pago': u'Los concepto deben coincidir (solo matricula o solo cuotas)' })
        return self.cleaned_data




class ReciboForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReciboForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial = datetime.now()
    class Media:
        css = {'all': ('/static/admin/css/forms.css',),}
        js = ('/admin/jsi18n',)

    class Meta:
        model = Recibo
        exclude = [ 'monto',  'estado', 'motivo_anulacion']
        widgets = {
            'fecha': SelectDateWidget(years=range(1900, datetime.now().date().year + 1, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'serie' : forms.TextInput(attrs = {'class':'form-control',}),
            'nro_recibo' : forms.TextInput(attrs = { 'class':'form-control', 'placeholder':'Verifique nro de recibo', 'autofocus' : 'autofocus', 'autocomplete' : 'off' }),
            'persona' : ForeignKeyRawIdWidget(Recibo._meta.get_field('persona').rel, site),
            'cantidad' : forms.TextInput(attrs = {'class':'form-control'}),
            'concepto' : ForeignKeyRawIdWidget(Recibo._meta.get_field('concepto').rel, site),
        }

    def clean(self):
        nro_recibo = self.cleaned_data.get('nro_recibo')
        serie = self.cleaned_data.get('serie')
        if nro_recibo and serie:
            if Recibo.objects.filter(nro_recibo=nro_recibo, serie=serie):
                raise ValidationError({'nro_recibo': u'Ya existe un Recibo con el numero: %s de la serie: %s' % (str(nro_recibo), serie) })



class AnularReciboForm(forms.Form):
    motivo = forms.CharField(widget=forms.Textarea(attrs = { 'class':'form-control'} ), label='Motivo de la Anulacion', required=True)
    def clean_motivo(self):
        import pdb; pdb.set_trace()

class fracPlanPagoForm(forms.ModelForm):
    hasta = forms.CharField(widget=forms.TextInput(attrs = { 'class':'form-control'} ), label='Fraccionar en:', required=True)
    class Meta:
        model = PlanPago
        fields = ('hasta', 'vencimiento')
        widgets = {
            'vencimiento': SelectDateWidget(years=range(2000, datetime.now().date().year + 2, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
        }

