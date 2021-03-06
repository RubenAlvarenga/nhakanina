#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_tables2 import SingleTableView, RequestConfig
from django.core.urlresolvers import reverse_lazy, reverse


from .models import Concepto, Periodo, Arancel, TipoConcepto
from .tables import ConceptosTable, PeriodosTable, ArancelesTable, TiposConceptosTable
from .forms import ConceptoForm, PeriodoForm, ArancelForm, TipoConceptoForm
from apps.functions import msg_render

from django.forms.util import ErrorList
from django.db import IntegrityError
from django.contrib import messages
from django.template import RequestContext



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


class ConceptoDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Concepto
    success_url=reverse_lazy('aranceles:lst_concepto')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El concepto <strong>"+unicode(self.object.concepto)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))


class PeriodoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Periodo
    table_class = PeriodosTable
    def get_queryset(self):
        table = super(PeriodoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(resolucion=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(PeriodoSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        context['notbuttonlist'] = True
        return context


class PeriodoDetailView(DetailView):
    model=Periodo
    template_name='aranceles/detPeriodo.html'
    def get_context_data(self, **kwargs):
        context = super(PeriodoDetailView, self).get_context_data(**kwargs)
        context['aranceles'] = Arancel.objects.filter(resolucion=context['periodo'])
        return context


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

class PeriodoUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=Periodo
    form_class = PeriodoForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = msg_render("Los datos del periodo %(resolucion)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('aranceles:det_periodo', args=(self.object.id, ))


class PeriodoDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Periodo
    success_url=reverse_lazy('aranceles:lst_periodo')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El periodo <strong>"+unicode(self.object.resolucion)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))



class ArancelSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Arancel
    table_class = ArancelesTable
    def get_queryset(self):
        table = super(ArancelSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(Q(concepto__concepto__icontains=q) | Q(concepto__tipo_concepto__tipo_concepto__titulo__icontains=q) )#.order_by(sort)
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

class ArancelUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=Arancel
    form_class = ArancelForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = msg_render("Los datos del arancel para %(concepto)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('aranceles:det_arancel', args=(self.object.id, ))

class ArancelDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Arancel
    success_url=reverse_lazy('aranceles:lst_arancel')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El arancel para <strong>"+unicode(self.object.concepto)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))



class TipoConceptoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = TipoConcepto
    table_class = TiposConceptosTable
    def get_queryset(self):
        table = super(TipoConceptoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(Q(titulo__icontains=q) )#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(TipoConceptoSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        context['notbuttonlist'] = True
        return context

class TipoConceptoDetailView(DetailView):
    model=TipoConcepto
    template_name='aranceles/detTipoConcepto.html'
    def get_context_data(self, **kwargs):
        context = super(TipoConceptoDetailView, self).get_context_data(**kwargs)
        return context


class TipoConceptoCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = TipoConceptoForm
    success_message = msg_render("%(titulo)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('aranceles:det_tipoconcepto', args=(self.object.id, ))
    

class TipoConceptoUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=TipoConcepto
    form_class = TipoConceptoForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = msg_render("%(titulo)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('aranceles:det_tipoconcepto', args=(self.object.id, ))


class TipoConceptoDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=TipoConcepto
    success_url=reverse_lazy('aranceles:lst_tipoconcepto')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"<strong>"+unicode(self.object.titulo)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))
