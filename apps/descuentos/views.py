#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django_tables2 import SingleTableView, RequestConfig
from django.template import RequestContext
from django.db.models import Q
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime
from django.forms.extras.widgets import SelectDateWidget


from apps.functions import msg_render
from wkhtmltopdf.views import PDFTemplateResponse
from apps.actions import export_as_csv, export_table_to_csv, eliminar_bulk
from django.forms.util import ErrorList
from django.db import IntegrityError
from apps.decorators import custom_permission_required

from .models import Descuento
from .tables import DescuentoTable, DescuentoTablePDF
from .forms import DescuentoForm

from apps.entidades.models import Persona

class DescuentoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Descuento
    table_class = DescuentoTable
    def get_queryset(self):
        table = super(DescuentoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(motivo__icontains=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(DescuentoSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        return context

    def post(self, request, *args, **kwargs):
        checks = request.POST.getlist('checks')
        if not checks:
            mensaje = msg_render("<strong>Favor seleccione por lo menos un item</strong>")
            messages.add_message(request, messages.INFO, mensaje)
            url = request.META['HTTP_REFERER']
            return HttpResponseRedirect(url)

        sort=request.POST.get('sort')
        ids = map(int, checks)
        descuentos=Descuento.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = DescuentoTablePDF(descuentos)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(Descuento, request, table)

        elif accion=='A pdf':
            table.model=self.model
            RequestConfig(request).configure(table)    
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request , pdf_name, {'table':table, 'request': self.get_context_data.im_self.request})

        elif accion=='Eliminar':
            perm = 'descuentos.delete_descuento'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, descuentos)
                else:
                    dic={'object_list':descuentos}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)

class DescuentoCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = DescuentoForm
    success_message = msg_render("El descuento %(motivo)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('descuentos:det_descuento', args=(self.object.id, ))
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return super(DescuentoCreateView, self).form_valid(form)


class DescuentoDetailView(DetailView):
    model=Descuento
    template_name='descuentos/detDescuento.html'

class DescuentoUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=Descuento
    form_class = DescuentoForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = msg_render("Los datos del descuento %(motivo)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('descuentos:det_descuento', args=(self.object.id, ))


class DescuentoDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Descuento
    success_url=reverse_lazy('descuentos:lst_descuento')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El Descuento <strong>"+unicode(self.object.motivo)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))



def es_socio_afemec(request):
    try: persona = Persona.objects.get(pk=int(request.POST['id_persona']))
    except: persona = Persona.objects.get(pk=int(request.POST['persona']))
    if persona.socio_afemec: return True
    else: return False

def es_docente_ise(request):
    try: persona = Persona.objects.get(pk=int(request.POST['id_persona']))
    except: persona = Persona.objects.get(pk=int(request.POST['persona']))
    if persona.docente_ise: return True
    else: return False