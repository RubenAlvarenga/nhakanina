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
from .models import Curso, Materia, CursoMateria, CursoAlumno, Carrera
from .tables import CursosTable, CursosTablePDF, CarrerasTable, CarrerasTablePDF, MateriasTable, MateriasTablePDF 
from .forms import CursoForm, CursoAlumnoForm, CarreraForm, MateriaForm
from apps.aranceles.models import Arancel
from apps.functions import msg_render
from wkhtmltopdf.views import PDFTemplateResponse
from apps.actions import export_as_csv, export_table_to_csv, eliminar_bulk
from django.forms.util import ErrorList
from django.db import IntegrityError
from apps.decorators import custom_permission_required


class MateriaSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Materia
    table_class = MateriasTable
    def get_queryset(self):
        table = super(MateriaSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(nombre__icontains=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(MateriaSingleTableView, self).get_context_data(**kwargs)
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
        materias=Materia.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = MateriasTablePDF(materias)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(Materia, request, table)

        elif accion=='A pdf':
            table.model=self.model
            RequestConfig(request).configure(table)    
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request , pdf_name, {'table':table, 'request': self.get_context_data.im_self.request})

        elif accion=='Eliminar':
            perm = 'catedras.delete_carrera'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, materias)
                else:
                    dic={'object_list':materias}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)


class MateriaCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = MateriaForm
    success_message = msg_render("La Materia %(nombre)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('catedras:det_materia', args=(self.object.id, ))

class MateriaDetailView(DetailView):
    model=Materia
    template_name='catedras/detMateria.html'

class MateriaUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=Materia
    form_class = MateriaForm
    success_message = msg_render("La materia %(nombre)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('catedras:det_materia', args=(self.object.id, ))


class MateriaDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Materia
    success_url=reverse_lazy('catedras:lst_materia')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"La materia <strong>"+unicode(self.object.nombre)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))



class CarreraSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Carrera
    table_class = CarrerasTable
    def get_queryset(self):
        table = super(CarreraSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(nombre__icontains=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(CarreraSingleTableView, self).get_context_data(**kwargs)
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
        carreras=Carrera.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = CarrerasTablePDF(carreras)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(Curso, request, table)

        elif accion=='A pdf':
            table.model=self.model
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

        elif accion=='Eliminar':
            perm = 'catedras.delete_carrera'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, carreras)
                else:
                    dic={'object_list':carreras}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)


class CarreraCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = CarreraForm
    success_message = msg_render("La Carrera %(nombre)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('catedras:det_carrera', args=(self.object.id, ))

class CarreraDetailView(DetailView):
    model=Carrera
    template_name='catedras/detCarrera.html'


class CarreraUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=Carrera
    form_class = CarreraForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = msg_render("Los datos de la carrera %(nombre)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('catedras:det_carrera', args=(self.object.id, ))


class CarreraDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Carrera
    success_url=reverse_lazy('catedras:lst_carrera')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"La carrera <strong>"+unicode(self.object.nombre)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))


class CursoDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Curso
    success_url=reverse_lazy('catedras:lst_curso')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El curso <strong>"+unicode(self.object.carrera)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))



class CursoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Curso
    table_class = CursosTable
    def get_queryset(self):
        table = super(CursoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(carrera__nombre__icontains=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(CursoSingleTableView, self).get_context_data(**kwargs)
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
        cursos=Curso.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = CursosTablePDF(cursos)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(Curso, request, table)

        elif accion=='A pdf':
            table.model=Curso
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

        elif accion=='Eliminar':
            perm = 'catedras.delete_curso'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, cursos)
                else:
                    dic={'object_list':Cursos}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)





class CursoDetailView(DetailView):
    model=Curso
    template_name='catedras/detCurso.html'
    # def get_context_data(self, **kwargs):
    #     context = super(ReciboDetailView, self).get_context_data(**kwargs)
    #     context['totalenletras'] = num2words(self.object.monto, lang='es')
    #     return context

class CursoUpdateView(SuccessMessageMixin, UpdateView):
    template_name='catedras/addCurso.html'
    model=Curso
    form_class = CursoForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = "El Curso %(nombre)s modificado con exito"
    def get_success_url(self, instance):
        success_message = msg_render("El Curso <strong>%s(%s) %s %s</strong> Modificado con exito" % (str(instance.carrera), str(instance.inicio.year), str(instance.dias), str(instance.turno) ))
        messages.success(self.request, success_message)
        url = reverse('catedras:det_curso', kwargs={'pk': instance.id})
        return redirect(url)

    def get_form(self, form_class):
        form = super(CursoUpdateView,self).get_form(form_class) #instantiate using parent
        form.fields['matricula'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=1)
        form.fields['matricula_fpo'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=1)
        form.fields['monto_cuota'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=2)
        form.fields['examen_ordinario'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=3)
        form.fields['examen_extra'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=3)
        form.fields['aranceles'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=4)
        return form

    def form_valid(self, form):
        instance = form.save(commit=False)

        new_materias = form.cleaned_data['materias']
        new_examen_extra = form.cleaned_data['examen_extra']
        new_aranceles = form.cleaned_data['aranceles']
        new_dias = form.cleaned_data['dias']

        old_materias = self.object.materias.all()
        old_examen_extra = self.object.examen_extra.all()
        old_aranceles = self.object.aranceles.all()
        old_dias = self.object.dias.all()


        aborrar_materias = set(old_materias) - set(new_materias)
        aborrar_examen_extra = set(old_examen_extra) -set(new_examen_extra)
        aborrar_aranceles = set(old_aranceles) - set(new_aranceles)
        aborrar_dias = set(old_dias) - set(new_dias)


        aagregar_materias = set(new_materias) - set(old_materias) 
        aagregar_examen_extra = set(new_examen_extra) - set(old_examen_extra)
        aagregar_aranceles = set(new_aranceles) - set(old_aranceles) 
        aagregar_dias = set(new_dias) - set(old_dias) 



        for examen in aborrar_examen_extra:
            self.object.examen_extra.remove(examen)
        for arancel in aborrar_aranceles:
            self.object.aranceles.remove(arancel)
        for materia in aborrar_materias: 
            #VERIFICAR MATERIAS:
            curso_materia = CursoMateria.objects.get(materia=materia, curso=instance)
            curso_materia.delete()
        for dia in aborrar_dias:
            self.object.dias.remove(dia)


        for examen_arancel in aagregar_examen_extra:
            instance.examen_extra.add(examen_arancel)
        for arancel in aagregar_aranceles: 
            instance.aranceles.add(arancel)        
        for materia in aagregar_materias: 
            #VERIFICAR MATERIAS
            if not CursoMateria.objects.filter(materia=materia, curso=instance):
                curso_materia = CursoMateria(materia=materia, curso=instance)
                curso_materia.save()
        for dia in aagregar_dias: 
            instance.dias.add(dia)        
        
        instance.save()
        #return HttpResponseRedirect(self.success_url)
        return self.get_success_url(instance)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Corrija los Errores.', extra_tags='danger')
        return super(CursoUpdateView, self).form_invalid(form)



class CursoCreateView(SuccessMessageMixin, CreateView):
    template_name='catedras/addCurso.html'
    form_class = CursoForm
    # success_message = "El Curso %(carrera)s registrado con exito"
    # success_url=reverse_lazy('catedras:lst_curso')
    def get_success_url(self, instance):
        success_message = msg_render("El Curso <strong>%s %s %s</strong> registrado con exito" % (str(instance.carrera), str(instance.dias), str(instance.turno) ))
        messages.success(self.request, success_message)
        url = reverse('catedras:det_curso', kwargs={'pk': instance.id})
        return redirect(url)

    def get_form(self, form_class):
        form = super(CursoCreateView,self).get_form(form_class) #instantiate using parent
        form.fields['matricula'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=1)
        form.fields['matricula_fpo'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=1)
        form.fields['monto_cuota'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=2)
        form.fields['examen_ordinario'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=3)
        form.fields['examen_extra'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=3)
        form.fields['aranceles'].queryset = Arancel.objects.filter(concepto__tipo_concepto__tipo_concepto=4)
        return form

    def form_valid(self, form):
        instance = form.save(commit=False)
        materias = form.cleaned_data['materias']
        examen_extra = form.cleaned_data['examen_extra']
        aranceles = form.cleaned_data['aranceles']
        dias = form.cleaned_data['dias']
        instance.save()

        for dia in dias: 
            instance.dias.add(dia)
        for examen_arancel in examen_extra: 
            instance.examen_extra.add(examen_arancel)
        for arancel in aranceles: 
            instance.aranceles.add(arancel)
        for materia in materias:
            curso_materia = CursoMateria(materia=materia, curso=instance)
            curso_materia.save()
        #return HttpResponseRedirect(self.success_url)
        return self.get_success_url(instance)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Corrija los Errores.', extra_tags='danger')
        return super(CursoCreateView, self).form_invalid(form)


class CursoAlumnoCreateView(SuccessMessageMixin, CreateView):
    template_name='catedras/addCursoAlumno.html'
    form_class = CursoAlumnoForm
    #success_message = "El Curso %(carrera)s registrado con exito"
    #success_url=reverse_lazy('entidades:lst_curso')
    def get_success_url(self, instance):
        success_message = msg_render("El Alumno <strong>%s</strong> inscripto al curso <strong>%s</strong> con exito" % (str(instance.alumno), str(instance.curso) ))
        messages.success(self.request, success_message)
        url = reverse('entidades:det_alumno', kwargs={'pk': instance.alumno.codigo})
        return redirect(url)

    def get_form(self, form_class):
        form = super(CursoAlumnoCreateView,self).get_form(form_class) #instantiate using parent
        form.fields['curso'].queryset = Curso.objects.filter(estado=True)
        return form


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return self.get_success_url(instance)


    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Corrija los Errores.', extra_tags='danger')
        return super(CursoAlumnoCreateView, self).form_invalid(form)




@custom_permission_required('finanzas.changue_planpago')
def recuperarPlan(request, pk):
    curso_alumno = CursoAlumno.objects.get(pk=int(pk))
    curso_alumno.save()
    mensaje = msg_render("<strong>Plan Recuperado con exito</strong>")
    messages.add_message(request, messages.SUCCESS, mensaje)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])   


def get_full_curso_ajax(request):
    id_curso = request.GET['id_curso']
    try : curso = get_object_or_404(Curso, id=int(id_curso))
    except: curso = False
    if curso: data = curso
    else: data = "No existe"
    return HttpResponse(data)
