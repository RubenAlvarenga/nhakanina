#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Rendicion
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import FilteredSelectMultiple, ForeignKeyRawIdWidget

from datetime import datetime

class RendicionForm(forms.ModelForm):
    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/jsi18n',)

    class Meta:
        model = Rendicion
        exclude = ('estado', 'total', 'fecha_aprobacion')
        widgets = {
			'nro_rendicion' : forms.TextInput(attrs = {'class':'form-control'}),
            #'fecha_aprobacion': SelectDateWidget(years=range(datetime.now().date().year, datetime.now().date().year + 3, 1), attrs = {'class':'form-control', 'style':'width:100px; float:left'}),
            'recibos' : FilteredSelectMultiple("Recibos", is_stacked=False, attrs = {'class':'form-control'}),
        }
