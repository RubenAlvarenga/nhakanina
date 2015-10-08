#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django_tables2 import SingleTableView, RequestConfig
from django.template import RequestContext
from django.db.models import Q
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime
from django.forms.extras.widgets import SelectDateWidget
from apps.entidades.models import Alumno, Persona
from apps.finanzas.models import PlanPago, Recibo, ReciboPlanPago
from apps.aranceles.models import Arancel
from apps.catedras.models import CursoAlumno, Materia
from .tables import AlumnosTable, PersonasTable, PlanPagoTable, PlanPagoAplReciboTable, RecibosTable, RecibosTablePDF, \
    CursosTable, ExtractoCursoAlumnoTable
from .functions import fracionar_plan, msg_render, sumarTotalesPlanPago
from .forms import ReciboPlanPagoForm, ReciboForm, PlanPagoForm, updPlanPagoForm
from apps.catedras.models import Curso
from apps.actions import export_as_csv, export_table_to_csv
from django import forms
from apps.decorators import custom_permission_required
from wkhtmltopdf.views import PDFTemplateResponse
from django.forms.util import ErrorList
from django.db import IntegrityError
from apps.prints import imprimir_recibo


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
        context['notbuttonlist'] = True
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



class AlumnoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Alumno
    table_class = AlumnosTable
    def get_queryset(self):
        table = super(AlumnoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: 
	        if q.isdigit(): return table.filter(cedula=q)#.order_by(sort)
	        else: return table.filter(apellido1__icontains=q)#.order_by(sort)
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
        

class AlumnoDetailView(DetailView):
    model=Alumno
    template_name='finanzas/detAlumno.html'        
    def get_context_data(self, **kwargs):
        context = super(AlumnoDetailView, self).get_context_data(**kwargs)
        recibos = Recibo.objects.filter(persona=self.object)
        recibossueltos = []
        for recibo in recibos:
            if recibo.get_planes == False:
                recibossueltos.append(recibo)
        context['recibossueltos'] = recibossueltos
        return context

class PersonaDetailView(DetailView):
    model=Persona
    template_name='finanzas/detPersona.html'

    def get_context_data(self, **kwargs):
        context = super(PersonaDetailView, self).get_context_data(**kwargs)
        context['aranceles'] = Arancel.objects.filter(resolucion__estado='ACT')
        return context



from num2words import num2words
class ReciboDetailView(DetailView):
    model=Recibo
    template_name='finanzas/detRecibo.html'        
    def get_context_data(self, **kwargs):
        context = super(ReciboDetailView, self).get_context_data(**kwargs)
        context['totalenletras'] = num2words(self.object.monto, lang='es')
        return context




from django.utils.dateparse import parse_date
class PlanPagoFormView(SuccessMessageMixin, FormView):
    template_name='finanzas/addPlanPago.html'
    form_class = PlanPagoForm
    #success_message = "El recibo %(serie)s %(nro_recibo)s registrado con exito"
    def get_success_url(self, instance):
        success_message = msg_render("El Plan Pago para <strong>%s</strong> registrado con exito" % (str(instance.curso_alumno)))
        messages.success(self.request, success_message)
        url = reverse('finanzas:det_persona', kwargs={'pk': instance.curso_alumno.alumno.id})
        return redirect(url)

    def get_form(self, form_class):
        form = super(PlanPagoFormView,self).get_form(form_class) #instantiate using parent
        #form.fields['materia'].queryset = Materia.objects.filter(pk=0)
        return form


    def form_valid(self, form):
        instance = form.save(commit=False)
        #import pdb; pdb.set_trace()
        instance.monto = instance.cantidad * instance.concepto.monto
        instance.created_by = self.request.user
        if not instance.secuencia:
            ultimasecuencia = PlanPago.objects.filter(curso_alumno=instance.curso_alumno, concepto=instance.concepto).order_by('-secuencia')
            if ultimasecuencia: instance.secuencia = ultimasecuencia[0].secuencia + 1
            else: instance.ultimasecuencia = 0
        instance.save()
        return self.get_success_url(instance)
        #return super(PlanPagoFormView, self).form_valid(form)
    
    def form_invalid(self, form):
        if form.cleaned_data.get('curso_alumno'): form.fields['materia'].queryset = form.cleaned_data.get('curso_alumno').curso.materias.all()
        messages.info(self.request,"Corrija los Errores")
        return super(PlanPagoFormView, self).form_invalid(form)



class ReciboFormView(SuccessMessageMixin, FormView):
    template_name='finanzas/addRecibo.html'
    form_class = ReciboForm
    #success_message = "El recibo %(serie)s %(nro_recibo)s registrado con exito"
    def get_success_url(self, instance):
        success_message = msg_render("El recibo <strong>%s-%s</strong> registrado con exito" % (str(instance.serie), str(instance.nro_recibo)))
        messages.success(self.request, success_message)
        url = reverse('finanzas:det_recibo', kwargs={'pk': instance.id})
        return redirect(url)


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.monto = instance.cantidad * instance.concepto.monto
        instance.cajero = self.request.user
        instance.save()
        imprimir_recibo(instance)
        return self.get_success_url(instance)
        #return super(ReciboFormView, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request,"Corrija los Errores")
        if form['persona'].value(): form.fields['persona'].queryset = Persona.objects.filter(pk=form['persona'].value())
        return super(ReciboFormView, self).form_invalid(form)

@custom_permission_required('finanzas.add_planpago')
def genPlanPago(request):
    if request.method == "POST":
        if request.POST['id_cursoalumno'] and not request.POST['id_arancel']:
            mensaje = msg_render("<strong>Favor seleccione el arancel para generar el Plan de Pago</strong>")
            messages.add_message(request, messages.INFO, mensaje)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])    
        if request.POST['id_cursoalumno'] and request.POST['id_arancel']:
            #CREAR PLAN
            curso_alumno = get_object_or_404(CursoAlumno, pk=int(request.POST['id_cursoalumno']))
            arancel = get_object_or_404(Arancel, pk=int(request.POST['id_arancel']) )
            form = PlanPagoForm(initial={"curso_alumno": curso_alumno, "concepto": arancel})
            form.fields['curso_alumno'].queryset = CursoAlumno.objects.filter(pk=curso_alumno.id)
            # form.fields['persona'].widget.attrs['disabled'] = 'disabled'
            # form.fields['concepto'].widget.attrs['disabled'] = 'disabled'
            template_name='finanzas/addPlanPago.html'
            dic={'object_list':form}
            return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))

@custom_permission_required('finanzas.add_recibo')
def genRecibo(request):
    if request.method == "POST":
        if request.POST['id_persona'] and not request.POST['id_arancel']:
            mensaje = msg_render("<strong>Favor seleccione el arancel </strong>")
            messages.add_message(request, messages.INFO, mensaje)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])    
        if request.POST['id_persona'] and request.POST['id_arancel']:
            #RECIBO SIN PLAN
            persona = get_object_or_404(Persona, pk=int(request.POST['id_persona']))
            arancel = get_object_or_404(Arancel, pk=int(request.POST['id_arancel']) )
            form = ReciboForm(initial={"fecha":datetime.now(), "persona": persona, "concepto": arancel})
            # form.fields['persona'].widget.attrs['disabled'] = 'disabled'
            # form.fields['concepto'].widget.attrs['disabled'] = 'disabled'
            form.fields['persona'].queryset = Persona.objects.filter(pk=persona.id)
            template_name='finanzas/addRecibo.html'
            dic={'object_list':form}
            return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))

@custom_permission_required('finanzas.add_recibo')
def genReciboPlanPago(request):
    if request.method == "POST":
        checks = request.POST.getlist('plan_pago')
        if not checks:
            mensaje = msg_render("<strong>Favor seleccione por lo menos un item</strong>")
            messages.add_message(request, messages.INFO, mensaje)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            ids = map(int, checks)
            planes = PlanPago.objects.filter(pk__in=ids)
            conceptos=[]
            for plan in planes: conceptos.append(plan.concepto.concepto)
            if len(set(conceptos)) > 1:
                mensaje = msg_render("<strong>Favor seleccione solamente un concepto</strong>")
                messages.add_message(request, messages.INFO, mensaje)
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                persona = get_object_or_404(Persona, pk=int(request.POST['id_persona']))
                form = ReciboPlanPagoForm(initial={"persona": persona, "plan_pago" : planes })
                #form.fields['persona'].widget.attrs['disabled'] = 'disabled'
                form.fields['plan_pago'].widget = forms.CheckboxSelectMultiple({"checked":'checked'})
                form.fields['plan_pago'].queryset = planes 
                form.fields['persona'].queryset = Persona.objects.filter(pk=persona.id)
                template_name='finanzas/addReciboPlanPago.html'
                # GENERAR TOTALES
                total = sumarTotalesPlanPago(planes)
                dic={'object_list':form, 'total' : total}
                return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))

@custom_permission_required('finanzas.change_planpago')
def aplReciboPlanPago(request, pk):
    dic={}
    template_name="finanzas/aplReciboPlanPago.html"
    recibo = get_object_or_404(Recibo, id=int(pk))
    if request.method == "POST":
        checks= request.POST.getlist('checks')
        if not checks:
            mensaje = msg_render("<strong>Favor seleccione por lo menos un item</strong>")
            messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            ids = map(int, checks)
            planesseleccionados = PlanPago.objects.filter(pk__in=ids)
            if recibo.cantidad != len(planesseleccionados):
                mensaje = msg_render("<strong>Cantidades NO COINCIDEN</strong>")
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            totales=0
            for plan in planesseleccionados:
                if recibo.concepto != plan.concepto:
                    mensaje = msg_render("<strong>Conceptos NO COINCIDEN</strong>")
                    messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    totales = totales + plan.monto
            if recibo.monto != totales:
                mensaje = msg_render("<strong>Montos NO COINCIDEN</strong>")
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                #CORRECTISIMO
                reciboplan = ReciboPlanPago(recibo_ptr_id=recibo.pk)
                reciboplan.__dict__.update(recibo.__dict__)
                reciboplan.save()
                for plana in planesseleccionados: reciboplan.plan_pago.add(plana)
                reciboplan.save()
                mensaje = msg_render("<strong>Recibo %s-%s Aplicado a Planes con Éxito</strong>" % (unicode(recibo.serie), unicode(recibo.nro_recibo)))
                messages.add_message(request, messages.SUCCESS, mensaje)
                url = reverse_lazy('finanzas:det_recibo', args=(recibo.id, ))
                return HttpResponseRedirect(url)
    else:
        if recibo.estado=='ANU':
            mensaje = msg_render("<strong>El recibo está Anulado imposible asignar a plan</strong>")
            messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])            
        else:
            planes = PlanPago.objects.filter(concepto=recibo.concepto, curso_alumno__alumno=recibo.persona.es_alumno, estado='PEN')
            if not planes:
                mensaje = msg_render("<strong>No existe Planes con el concepto %s</strong>" % unicode(recibo.concepto))
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                table = PlanPagoAplReciboTable(planes)
                dic['recibo']=recibo
                dic['planes']=table
                return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))



def total_recibo_plan_pago_ajax(request):
    if request.is_ajax():
        checks= request.GET.getlist('checks[]')
        ids = map(int, checks)
        planes = PlanPago.objects.filter(pk__in=ids)
        total = sumarTotalesPlanPago(planes)
        return HttpResponse(intcomma(int(total)))

class ReciboSingleTableView(SingleTableView):
    template_name='finanzas/lstRecibo.html'
    model = Recibo
    table_class = RecibosTable
    def get_queryset(self):
        table = super(ReciboSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: 
            # if q.isdigit(): return table.filter(nro_recibo=q)#.order_by(sort)
            # else: return table.filter(persona__apellido1__icontains=q)#.order_by(sort)
            if q.isdigit(): return table.filter(nro_recibo=q)#.order_by(sort)
            else: return table.filter(Q(persona__apellido1__icontains=q) | Q(persona__apellido2__icontains=q) | Q(persona__nombre1__icontains=q) | Q(persona__nombre2__icontains=q))#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(ReciboSingleTableView, self).get_context_data(**kwargs)
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
        recibos=Recibo.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')

        table = RecibosTablePDF(recibos)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(Recibo, request, table)

        elif accion=='A pdf':
            table.model=Recibo
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

        elif accion=='Eliminar':
            mensaje = "ACCESO RESTRINGIDO | solo es posible la Anulacion"
            messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
            url = request.META['HTTP_REFERER']
            return HttpResponseRedirect(url)

class ReciboPlanPagoFormView(SuccessMessageMixin, FormView):
    template_name='finanzas/addReciboPlanPago.html'
    form_class = ReciboPlanPagoForm
    #success_message = "El recibo %(serie)s %(nro_recibo)s registrado con exito"
    def get_success_url(self, instance):
        success_message = msg_render("El recibo <strong>%s-%s</strong> registrado con exito" % (str(instance.serie), str(instance.nro_recibo)))
        messages.success(self.request, success_message)
        url = reverse('finanzas:det_recibo', kwargs={'pk': instance.id})
        return redirect(url)

    def form_valid(self, form):
        instance = form.save(commit=False)
        total=0
        if len(form.cleaned_data['plan_pago']) == 1:
            cantidad = form.cleaned_data['plan_pago'][0].cantidad
            total = form.cleaned_data['plan_pago'][0].monto
            concepto = form.cleaned_data['plan_pago'][0].concepto
        else:
            concepto=[]
            for p in form.cleaned_data['plan_pago']:
                total=total+p.monto
                concepto.append(p.concepto)
            if len(set(concepto)) == 1:
                concepto = set(concepto).pop()
            cantidad = len(form.cleaned_data['plan_pago'])

        instance.monto = total
        instance.concepto = concepto
        instance.cantidad = cantidad
        instance.cajero = self.request.user
        instance.save()
        form.save_m2m()
        return self.get_success_url(instance)
        #return super(ReciboPlanPagoFormView, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request,"Corrija los Errores")
        if form['plan_pago'].value():
            form.fields['plan_pago'].queryset = form.clean()['plan_pago']    
        else:
            form.fields['plan_pago'].queryset = []
        if form['persona'].value(): form.fields['persona'].queryset = Persona.objects.filter(pk=form['persona'].value())
        else: 
            planes = form.clean()['plan_pago']
            form.fields['persona'].queryset = Persona.objects.filter(pk=planes[0].curso_alumno.alumno.id)

        #form.fields['persona'].widget.attrs['disabled'] = 'disabled'
        return super(ReciboPlanPagoFormView, self).form_invalid(form)




  


@custom_permission_required('finanzas.add_planpago')
def fraccionar_planpago_ajax(request):
    if request.is_ajax():
        if request.POST['id_planpago']:
            plan_pago = PlanPago.objects.get(pk=int(request.POST['id_planpago']))
            cantidad = int(request.POST['cantidad'])
            mensaje=''
            if cantidad > plan_pago.concepto.concepto.fraccionable_hasta or cantidad==1:
                mensaje = "La cantidad máxima para este concepto es: "+str(plan_pago.concepto.concepto.fraccionable_hasta)+' cuotas'
            else:
                if not plan_pago.vencimiento:
                    mensaje = "Error: El Plan de pago debe tener fecha del 1er vencimiento"
                else:
                    fraccionado = fracionar_plan(plan_pago, cantidad, request.user)
                    if not fraccionado: 
                        mensaje = "Ocurrio un Error Inesperado"
                    else:
                        return HttpResponse("success")
        template='finanzas/fraccionar_form.html'
    return render_to_response(template, {'mensaje': mensaje})




from .forms import AnularReciboForm
class ReciboCancelView(SuccessMessageMixin, DeleteView):
    """
    Clase Importante no modificar
    Afecta la anulacion de recibos a planes de pago
    """
    template_name='finanzas/anuRecibo.html'
    model=Recibo
    success_url=reverse_lazy('finanzas:lst_recibo')
    def get_context_data(self, **kwargs):
        context = super(ReciboCancelView, self).get_context_data(**kwargs)
        context['form'] = AnularReciboForm()
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.rendido:
            print "ya esta rendido"
        else:
            if not request.POST['motivo'].strip():
                mensaje = msg_render("<strong>Favor introduzca el motivo de la anulacion</strong>")
                messages.add_message(request, messages.INFO, mensaje)
                return HttpResponseRedirect(request.META['HTTP_REFERER'])  
            else:
                if self.object.get_planes:
                    #ES RECIBOPLANPAGO
                    self.object = self.object.get_planes
                    self.object.estado='ANU'
                    self.object.motivo_anulacion = request.POST['motivo']
                    self.object.fecha_anulacion = datetime.now()
                    self.object.usuario_anulacion = request.user
                    self.object.monto = 0
                    self.object.save()

                else:
                    self.object.estado='ANU'
                    self.object.motivo_anulacion = request.POST['motivo']
                    self.object.fecha_anulacion = datetime.now()
                    self.object.usuario_anulacion = request.user
                    self.object.monto = 0
                    self.object.save()
                success_message = msg_render("El recibo <strong>"+str(self.object)+"</strong> ha sido anulado")
                messages.add_message(request, messages.SUCCESS, success_message )
                return HttpResponseRedirect(self.get_success_url(), )

        # import pdb; pdb.set_trace()
        # try:
        #     self.object.delete()
        # except IntegrityError as e:
        #     e.tags='danger'
        #     dic={'messages': (e,), 'object': self.object}
        #     return render_to_response(self.template_name, dic, context_instance=RequestContext(request))




class PlanPagoSingleTableView(SingleTableView):
    template_name='finanzas/lstPlanPago.html'
    model = PlanPago
    table_class = PlanPagoTable
    def get_queryset(self):
        table = super(PlanPagoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: 
            if q.isdigit(): return table.filter(curso_alumno__alumno__cedula=q)#.order_by(sort)
            else: return table.filter(Q(curso_alumno__alumno__apellido1__icontains=q) | Q(curso_alumno__alumno__apellido2__icontains=q) | Q(curso_alumno__alumno__nombre1__icontains=q) | Q(curso_alumno__alumno__nombre2__icontains=q))#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(PlanPagoSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        context['notbuttonlist'] = True
        return context

    # def post(self, request, *args, **kwargs):
    #     checks = request.POST.getlist('checks')
    #     if not checks:
    #         mensaje = msg_render("<strong>Favor seleccione por lo menos un item</strong>")
    #         messages.add_message(request, messages.INFO, mensaje)
    #         url = request.META['HTTP_REFERER']
    #         return HttpResponseRedirect(url)

    #     sort=request.POST.get('sort')
    #     ids = map(int, checks)
    #     alumnos=Alumno.objects.filter(pk__in=ids)
    #     accion=request.POST.get('accion')




class PlanPagoDetailView(DetailView):
    model=PlanPago
    template_name='finanzas/detPlanPago.html'

class PlanPagoUpdateView(SuccessMessageMixin, UpdateView):
    template_name='finanzas/updPlanPago.html'
    model=PlanPago
    form_class = updPlanPagoForm
    success_message = msg_render("El PlanPago %(curso_alumno)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('finanzas:det_planpago', args=(self.object.id, ))
    
    def get_form(self, form_class):
        form = super(PlanPagoUpdateView,self).get_form(form_class) #instantiate using parent
        form.fields['curso_alumno'].widget.attrs['disabled'] = 'disabled'
        form.fields['cantidad'].widget.attrs['disabled'] = 'disabled'
        form.fields['concepto'].widget.attrs['disabled'] = 'disabled'
        return form


    
    def form_invalid(self, form):
        if form.cleaned_data.get('curso_alumno'): form.fields['materia'].queryset = form.cleaned_data.get('curso_alumno').curso.materias.all()
        # form.fields['cantidad'].initial = self.request.POST['cantidad']
        # form.fields['curso_alumno'].initial = get_object_or_404(CursoAlumno, id=int(self.request.POST['curso_alumno']))
        # form.fields['concepto'].initial = int(self.request.POST['concepto'])
        messages.info(self.request,"Corrija los Errores")
        return super(PlanPagoUpdateView, self).form_invalid(form)




class PlanPagoDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=PlanPago
    success_url=reverse_lazy('finanzas:lst_planpago')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.estado=='PAG':
            mensaje = msg_render("<strong>El Plan de Pago esta PAGADO imposible eliminar</strong>")
            messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
            url = request.META['HTTP_REFERER']
            return HttpResponseRedirect(url)
        else:
            try:
                self.object.delete()
                success_message = msg_render(u"El Plande Pago <strong>"+unicode(self.object.concepto)+u"</strong> eliminado con éxito")
                messages.add_message(request, messages.SUCCESS, success_message )
                return HttpResponseRedirect(self.get_success_url(), )
            except IntegrityError as e:
                e.tags='danger'
                dic={'messages': (e,), 'object': self.object}
                return render_to_response(self.template_name, dic, context_instance=RequestContext(request))


def get_curso_alumno_ajax(request):
    id_curso_alumno = request.GET['id_curso_alumno']
    try: cursoalumno = get_object_or_404(CursoAlumno, id=id_curso_alumno)
    except: cursoalumno = False 
    if cursoalumno: data = msg_render("%s (%s) [%s]" % (unicode(cursoalumno.alumno), unicode(cursoalumno.alumno.cedula), unicode(cursoalumno.curso) ) ) 
    else: data = "No existe"
    return HttpResponse(data)

def get_concepto_ajax(request):
    id_arancel = request.GET['id_arancel']
    try: concepto = get_object_or_404(Arancel, id=id_arancel)
    except: concepto = False 
    if concepto: data = unicode(concepto)
    else: data = "No existe"
    return HttpResponse(data)


from django.core import serializers
def get_materias_ajax(request):
    id_curso_alumno = request.GET['id_curso_alumno']
    if id_curso_alumno:
        try: cursoalumno = get_object_or_404(CursoAlumno, id=id_curso_alumno)
        except: cursoalumno = False
        if cursoalumno: data = serializers.serialize('json', cursoalumno.curso.materias.all())
        else: data = "No existe"
        return HttpResponse(data, content_type='application/json')




class CursoExtractoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Curso
    table_class = CursosTable
    def get_queryset(self):
        table = super(CursoExtractoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(carrera__nombre__icontains=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(CursoExtractoSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        context['notbuttonlist'] = True
        return context




class CursoDetailView(DetailView):
    model=Curso
    template_name='finanzas/detCurso.html'
    def get_context_data(self, **kwargs):
        context = super(CursoDetailView, self).get_context_data(**kwargs)
        context['matriculas'] = PlanPago.objects.filter(curso_alumno__curso=context['object'], concepto__concepto__tipo_concepto__tipo_concepto__id=1)
        context['cuotas'] = PlanPago.objects.filter(curso_alumno__curso=context['object'], concepto__concepto__tipo_concepto__tipo_concepto__id=2).order_by('curso_alumno', 'secuencia')
        context['evaluacion'] = PlanPago.objects.filter(curso_alumno__curso=context['object'], concepto__concepto__tipo_concepto__tipo_concepto__id=3)
        return context


def imprimirExtracto(request):
    pdf_name = 'finanzas/reportes/pdfExtracto.html'
    checks = request.POST.getlist('curso_alumno_id')
    if not checks:
        mensaje = msg_render("<strong>Favor seleccione por lo menos un item</strong>")
        messages.add_message(request, messages.INFO, mensaje)
        url = request.META['HTTP_REFERER']
        return HttpResponseRedirect(url)
    else:
        dic={}
        dic['impresoel']=datetime.now()
        dic['impresopor'] = request.user
        curso_planes = []
        ids = map(int, checks)
        for id in ids:
            planes=PlanPago.objects.filter(curso_alumno=id).order_by("vencimiento", "concepto__concepto__tipo_concepto__tipo_concepto__id")
            table = ExtractoCursoAlumnoTable(planes)
            table.curso=unicode(planes[0].curso_alumno.curso)
            RequestConfig(request).configure(table)            
            curso_planes.append(table)

        dic['alumno'] = PlanPago.objects.filter(curso_alumno__in=ids).distinct('curso_alumno__alumno')[0].curso_alumno.alumno
        dic['curso_planes'] = curso_planes
        
        return PDFTemplateResponse(request, pdf_name, dic)
        