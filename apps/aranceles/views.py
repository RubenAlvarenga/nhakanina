#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_tables2 import SingleTableView, RequestConfig
from django.core.urlresolvers import reverse_lazy, reverse


from .models import Concepto, Periodo, Arancel
from .tables import ConceptosTable, PeriodosTable, ArancelesTable
from .forms import ConceptoForm, PeriodoForm, ArancelForm
from apps.functions import msg_render


class ConceptoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Concepto
    table_class = ConceptosTable
    def get_queryset(self):
        table = super(ConceptoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(Q(concepto__icontains=q) | Q(tipo_concepto__tipo_concepto__titulo__icontains=q) )#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(ConceptoSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        context['notbuttonlist'] = True
        return context


class ConceptoDetailView(DetailView):
    model=Concepto
    template_name='aranceles/detConcepto.html'


class ConceptoCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = ConceptoForm
    success_message = msg_render("El concepto %(concepto)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('aranceles:det_concepto', args=(self.object.id, ))


class ConceptoUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=Concepto
    form_class = ConceptoForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = msg_render("Los datos del concepto %(concepto)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('aranceles:det_concepto', args=(self.object.id, ))



class PeriodoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Periodo
    table_class = PeriodosTable
    def get_queryset(self):
        table = super(PeriodoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(Q(concepto__icontains=q) | Q(tipo_concepto__tipo_concepto__titulo__icontains=q) )#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(PeriodoSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        context['notbuttonlist'] = True
        return context


class PeriodoDetailView(DetailView):
    model=Periodo
    template_name='aranceles/detPeriodo.html'


class PeriodoCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = PeriodoForm
    success_message = msg_render("El Periodo con Resolucion %(resolucion)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('aranceles:det_periodo', args=(self.object.id, ))
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return super(PeriodoCreateView, self).form_valid(form)


class ArancelSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Arancel
    table_class = ArancelesTable
    def get_queryset(self):
        table = super(ArancelSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(Q(concepto__icontains=q) | Q(tipo_concepto__tipo_concepto__titulo__icontains=q) )#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(ArancelSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        context['notbuttonlist'] = True
        return context

class ArancelDetailView(DetailView):
    model=Arancel
    template_name='aranceles/detArancel.html'

class ArancelCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = ArancelForm
    success_message = msg_render("El Arancel con Resolucion %(resolucion)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('aranceles:det_arancel', args=(self.object.id, ))
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return super(ArancelCreateView, self).form_valid(form)
