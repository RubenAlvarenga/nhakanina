#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404
from django.db.models import Q
from django_tables2 import SingleTableView, RequestConfig
from .models import Persona, Alumno
from .tables import PersonasTable, AlumnosTable, PersonasTablePDF, AlumnosTablePDF
from apps.functions import msg_render
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from wkhtmltopdf.views import PDFTemplateResponse
from apps.actions import export_as_csv, export_table_to_csv, eliminar_bulk
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .forms import PersonaForm, AlumnoForm
from django.template import RequestContext
from django.http import HttpResponse
from django.forms.util import ErrorList
from django.db import IntegrityError

class PersonaSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Persona
    table_class = PersonasTable
    def get_queryset(self):
        table = super(PersonaSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: 
            if q.isdigit(): return table.filter(cedula=q)#.order_by(sort)
            else: return table.filter(Q(apellido1__icontains=q) | Q(apellido2__icontains=q) | Q(nombre1__icontains=q) | Q(nombre2__icontains=q))#.order_by(sort)
        else: return table


    def get_context_data(self, **kwargs):
        context = super(PersonaSingleTableView, self).get_context_data(**kwargs)
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
        personas=Persona.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = PersonasTablePDF(personas)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(Persona, request, table)

        elif accion=='A pdf':
            table.model=Persona
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

        elif accion=='Eliminar':
            perm = 'entidades.delete_persona'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, personas)
                else:
                    dic={'object_list':personas}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)

class PersonaCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = PersonaForm
    success_message = msg_render("La Persona %(nombre1)s %(apellido1)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('entidades:det_persona', args=(self.object.id, ))


class PersonaDetailView(DetailView):
    model=Persona
    template_name='entidades/detPersona.html'

class PersonaUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=Persona
    form_class = PersonaForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = msg_render("Los datos de %(nombre1)s %(apellido1)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('entidades:det_persona', args=(self.object.id, ))

class PersonaDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Persona
    success_url=reverse_lazy('entidades:lst_persona')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"La Persona <strong>"+unicode(self.object.apellido1)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))



class AlumnoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Alumno
    table_class = AlumnosTable
    def get_queryset(self):
        table = super(AlumnoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: 
            if q.isdigit(): return table.filter(cedula=q)#.order_by(sort)
            else: return table.filter(Q(apellido1__icontains=q) | Q(apellido2__icontains=q) | Q(nombre1__icontains=q) | Q(nombre2__icontains=q))#.order_by(sort)
        else: return table


    def get_context_data(self, **kwargs):
        context = super(AlumnoSingleTableView, self).get_context_data(**kwargs)
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
        alumnos=Alumno.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        table = AlumnosTablePDF(alumnos)
        if sort!='None':
            table.order_by = sort 
        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(alumnos, request, table)
        elif accion=='A pdf':
            table.model=Alumno
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})
        elif accion=='Eliminar':
            perm = 'alumno.delete_alumno'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, alumnos)
                else:
                    dic={'object_list':alumnos}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)




class AlumnoCreateView(SuccessMessageMixin, CreateView):
    template_name='entidades/addAlumno.html'
    form_class = AlumnoForm
    success_message = msg_render("El Alumno %(nombre1)s %(apellido1)s registrado con exito")
    def get_success_url(self, instance=None):
        if instance: return reverse_lazy('entidades:det_alumno', args=(instance.codigo, ))
        else: return reverse_lazy('entidades:det_alumno', args=(self.object.codigo, ))


    def form_invalid(self, form):
        try: persona = Persona.objects.get(cedula=self.request.POST['cedula'])
        except: persona = None
        alumno = Alumno.objects.filter(cedula=self.request.POST['cedula'])
        if persona and not alumno:
            alumno = Alumno(persona_ptr_id=persona.pk)
            alumno.__dict__.update(persona.__dict__)
            alumno.save()
            success_message = msg_render(u"El Alumno <strong>"+unicode(alumno.get_full_name)+u"</strong> agregado con éxito")
            messages.add_message(self.request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url( alumno ), )
        return super(AlumnoCreateView, self).form_invalid(form)
    


from django.core import serializers
def verificarCedula_ajax(request):
    nrocedula = request.GET['nrocedula']
    unapersona = get_object_or_404(Persona, cedula=nrocedula)
    if unapersona: 
        #import pdb; pdb.set_trace()
        data = serializers.serialize('json', [unapersona], fields={'nombre1', 'nombre2', 'apellido1', 'apellido2', 'cedula'} )
        return HttpResponse(data, content_type='application/json')



class AlumnoDetailView(DetailView):
    model=Alumno
    template_name='entidades/detAlumno.html'

class AlumnoUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=Alumno
    form_class = AlumnoForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = msg_render("Los datos de %(nombre1)s %(apellido1)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('entidades:det_alumno', args=(self.object.codigo, ))


class AlumnoDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Alumno
    success_url=reverse_lazy('entidades:lst_alumno')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El Alumno <strong>"+unicode(self.object.apellido1)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))




def get_full_name_ajax(request):
    id_alumno = request.GET['id_alumno']
    try : alumno = get_object_or_404(Alumno, codigo=int(id_alumno))
    except: alumno = False
    if alumno: data = alumno.get_full_name
    else: data = "No existe"
    return HttpResponse(data)

from django.contrib.humanize.templatetags.humanize import intcomma
def persona_get_full_name_ajax(request):
    id_persona = request.GET['id_persona']
    try : persona = get_object_or_404(Persona, id=int(id_persona))
    except: persona = False
    if persona: data = (persona.get_full_name, " ("+intcomma(int(persona.cedula))+")" )
    else: data = "No existe"
    return HttpResponse(data)