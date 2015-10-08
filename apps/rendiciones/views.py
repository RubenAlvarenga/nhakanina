#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_tables2 import SingleTableView, RequestConfig
from django.core.urlresolvers import reverse_lazy, reverse


from .models import Rendicion
from .tables import RendicionesTable
from .forms import RendicionForm
from apps.functions import msg_render

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


class RendicionCreateView(SuccessMessageMixin, CreateView):
    template_name='rendiciones/addRendicion.html'
    form_class = RendicionForm
    success_message = msg_render("la rendicion %(nro_rendicion)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('rendiciones:det_rendicion', args=(self.object.id, ))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return super(RendicionCreateView, self).form_valid(form)

