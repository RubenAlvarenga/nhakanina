#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Descuento






class DescuentoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change): 
        obj.created_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change): 
        if formset.model == Descuento:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.created_by = request.user
                instance.save()
        else:
            formset.save()              


admin.site.register(Descuento, DescuentoAdmin)
