#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_tables2 import SingleTableView, RequestConfig
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms.util import ErrorList
from django.db import IntegrityError
from django.contrib import messages
from apps.decorators import custom_permission_required
from datetime import datetime, date

from apps.actions import export_as_csv, export_table_to_csv, rendiciones_to_csv
from .models import Rendicion
from .tables import RendicionesTable, RecibosTable, RecibosTablePDF, RecibosTableCSV
from .forms import RendicionForm, AprobarRendicionForm
from apps.functions import msg_render
from apps.finanzas.models import Recibo


class RendicionSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Rendicion
    table_class = RendicionesTable
    def get_queryset(self):
        table = super(RendicionSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(nombre__icontains=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(RendicionSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        return context

class RendicionDetailView(DetailView):
    model=Rendicion
    template_name='rendiciones/detRendicion.html'
    def get_context_data(self, **kwargs):
        context = super(RendicionDetailView, self).get_context_data(**kwargs)
        context['table'] = RecibosTable(self.object.recibos.all().order_by('nro_recibo'))
        return context


class RendicionCreateView(SuccessMessageMixin, CreateView):
    template_name='rendiciones/selRecibosRendicion.html'
    form_class = RendicionForm
    success_message = msg_render("la rendicion %(nro_rendicion)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('rendiciones:det_rendicion', args=(self.object.id, ))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return super(RendicionCreateView, self).form_valid(form)

    def get_form(self, form_class):
        form = super(RendicionCreateView,self).get_form(form_class)
        form.fields['recibos'].required = True
        form.fields['recibos'].choices = [(t.id, str(t.serie+"-"+str(t.nro_recibo)+" "+str(t.fecha)+" "+t.concepto.concepto.concepto)) for t in Recibo.objects.filter(rendido=False) if t.get_rendido==False ]
        return form


class RendicionDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Rendicion
    success_url=reverse_lazy('rendiciones:lst_rendicion')
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.estado=='APR':
            mensaje = msg_render("La Rendicion esta Aprobada.... <strong>Imposible Eliminar</strong>")
            messages.add_message(self.request, messages.ERROR, mensaje, extra_tags='danger')
            url = self.request.META['HTTP_REFERER']
            return HttpResponseRedirect(url) 
        return super(RendicionDeleteView, self).get(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"La rendicion Nro. <strong>"+unicode(self.object.nro_rendicion)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))




class RendicionUpdateView(SuccessMessageMixin, UpdateView):
    template_name='rendiciones/selRecibosRendicion.html'
    model=Rendicion
    form_class = RendicionForm
    success_message = msg_render("La rendición Nro %(nro_rendicion)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('rendiciones:det_rendicion', args=(self.object.id, ))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.estado=='APR':
            mensaje = msg_render("La Rendicion esta Aprobada.... <strong>Imposible Editar</strong>")
            messages.add_message(self.request, messages.ERROR, mensaje, extra_tags='danger')
            url = self.request.META['HTTP_REFERER']
            return HttpResponseRedirect(url) 
        return super(RendicionUpdateView, self).get(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(RendicionUpdateView,self).get_form(form_class) #instantiate using parent
        form.fields['recibos'].required = True
        form.fields['recibos'].choices = [(t.id, str(t.serie+"-"+str(t.nro_recibo)+" "+str(t.fecha)+" "+t.concepto.concepto.concepto)) for t in Recibo.objects.filter()]
        return form


    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Corrija los Errores.', extra_tags='danger')
        return super(RendicionUpdateView, self).form_invalid(form)

@custom_permission_required('rendiciones.list_rendicion')
def csvRendicion(request, pk):
    rendicion=Rendicion.objects.get(pk=int(pk))
    recibos=rendicion.recibos.all().order_by('nro_recibo')
    table = RecibosTableCSV(recibos)
    RequestConfig(request).configure(table)
    return rendiciones_to_csv(Recibo, request, table)



class AprobarRendicionUpdateView(SuccessMessageMixin, UpdateView):
    template_name='rendiciones/aprRendicion.html'
    model=Rendicion
    form_class = AprobarRendicionForm
    form_valid_message = msg_render("La rendición Nro %(nro_rendicion)s aprobado con exito")
    def get_success_url(self, instance):
        success_message = msg_render("La rendición Nro <strong>%s</strong> Aprobado con exito" % (str(instance.nro_rendicion)))
        messages.success(self.request, success_message)
        url = reverse('rendiciones:det_rendicion', kwargs={'pk': instance.id})
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super(AprobarRendicionUpdateView, self).get_context_data(**kwargs)
        context['table'] = RecibosTable(self.object.recibos.all().order_by('nro_recibo'))
        context['date'] = datetime.now()        
        return context


    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Corrija los Errores.', extra_tags='danger')
        return super(AprobarRendicionUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.aprobado_por = self.request.user
        instance.estado = 'APR'
        instance.fecha_aprobacion = datetime.now()
        instance.save()
        #return super(AprobarRendicionUpdateView, self).form_valid(form)
        return self.get_success_url(instance)