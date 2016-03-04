#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, urlresolvers, render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
from django_tables2 import SingleTableView
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User, Group, Permission
from .tables import UsersTable, GroupsTable, UsersTablePDF
from .models import Perfil
from apps.decorators import custom_permission_required
from django.contrib import messages
from django.template import RequestContext
from django.db.models import Q
from .forms import UserForm, updUserForm, GroupForm, chgPasswordForm, updPerfilForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.util import ErrorList
from django.db import IntegrityError
from apps.functions import msg_render
from django_tables2 import SingleTableView, RequestConfig
from wkhtmltopdf.views import PDFTemplateResponse
from apps.actions import export_as_csv, export_table_to_csv, eliminar_bulk

class UserSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = User
    table_class = UsersTable
    def get_queryset(self):
        table = super(UserSingleTableView, self).get_queryset().exclude(username__in=('autogenerado', 'admin'))
        q=self.request.GET.get("q")
        if q: return table.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q) )#.order_by(sort)
        else: return table

    def post(self, request, *args, **kwargs):
        checks = request.POST.getlist('checks')
        if not checks:
            mensaje = msg_render("<strong>Favor seleccione por lo menos un item</strong>")
            messages.add_message(request, messages.INFO, mensaje)
            url = request.META['HTTP_REFERER']
            return HttpResponseRedirect(url)

        sort=request.POST.get('sort')
        ids = map(int, checks)
        usuarios=User.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = UsersTablePDF(usuarios)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(User, request, table)

        elif accion=='A pdf':
            table.model=self.model
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

        elif accion=='Eliminar':
            perm = 'auth.delete_user'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, usuarios)
                else:
                    dic={'object_list':usuarios}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)


class GroupSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = Group
    table_class = GroupsTable

    def get_queryset(self):
        table = super(GroupSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(name__icontains=q)
        else: return table
    def get_context_data(self, **kwargs):
        context = super(GroupSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        context['notbuttonlist']=True
        return context



@custom_permission_required('auth.add_user')
def addUsuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None, request.FILES)
        if form.is_valid():
            usuario=form.save()
            userPerfil=Perfil.objects.get(user_id=usuario.id)
            if request.FILES:
                userPerfil.avatar=request.FILES['avatar']
                userPerfil.save()
            # else:
            #     userPerfil.avatar="avatar_user/default.png"
            #     userPerfil.save()                
            success_message = "El Usuario "+str(usuario.username)+" creado con exito"
            messages.add_message(request, messages.SUCCESS, success_message)
            url = urlresolvers.reverse('autorizaciones:det_usuario', args=(usuario.id,))
            return HttpResponseRedirect(url)
        else:
           pass
    else:
        form = UserForm()

    template='autorizaciones/addUser.html'
    return render_to_response(template, {"form": form}, context_instance=RequestContext(request, locals()))



class UserDetailView(DetailView):
    model=User
    template_name='autorizaciones/detUser.html'
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        permisos = Permission.objects.filter(user=context['object'])
        permisos_grupo= Permission.objects.filter(group__user=context['object'])
        context['user_permissions'] = permisos
        context['user_group_permissions'] = permisos_grupo
        context['user'] = self.request.user    
        return context

class UserPerfilDetailView(DetailView):
    model=User
    template_name='autorizaciones/detPerfil.html'
    def get_context_data(self, **kwargs):
        if self.object == self.request.user:
            context = super(UserPerfilDetailView, self).get_context_data(**kwargs)
            return context
        else: raise Http404

class UserPerfilUpdateView(SuccessMessageMixin, UpdateView):
    template_name='autorizaciones/updPerfil.html'
    model=User
    form_class = updPerfilForm
    success_message = msg_render("El Usuario %(first_name)s %(last_name)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('autorizaciones:det_miperfil', args=(self.object.id, ))

    def get_context_data(self, **kwargs):
        if self.object == self.request.user:
            context = super(UserPerfilUpdateView, self).get_context_data(**kwargs)
            context['user'] = self.request.user
            return context
        else: raise Http404


    def get_form(self, form_class):
        form = super(UserPerfilUpdateView,self).get_form(form_class) #instantiate using parent
        try : impresora = Perfil.objects.get(user_id=self.object.id).impresora
        except : impresora = 'ninguna'
        form.fields['impresora'].initial = impresora
        return form



    def form_valid(self, form):
        userperfil, created = Perfil.objects.get_or_create(user_id=self.object.id)
        if self.request.FILES:
            userperfil.avatar=self.request.FILES['avatar']
        if self.request.POST:
            try: 
                userperfil.impresora=self.request.POST['impresora']
            except: pass
        userperfil.save()

        return super(UserPerfilUpdateView, self).form_valid(form)


class GroupDetailView(DetailView):
    model=Group
    template_name='autorizaciones/detGroup.html'
    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        permisos = context['object'].permissions.get_queryset()
        context['group_permissions']= permisos
        return context




class UserUpdateView(SuccessMessageMixin, UpdateView):
    template_name='autorizaciones/updUser.html'
    model=User
    form_class = updUserForm
    success_message = msg_render("El Usuario %(username)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('autorizaciones:det_usuario', args=(self.object.id, ))
    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user    
        return context

    def get_form(self, form_class):
        form = super(UserUpdateView, self).get_form(form_class) #instantiate using parent
        try : impresora = Perfil.objects.get(user_id=self.object.id).impresora
        except : impresora = 'Ninguna'
        form.fields['impresora'].initial = impresora
        return form

    def form_valid(self, form):
        #if self.request.FILES:
            # userperfil, created = Perfil.objects.get_or_create(user_id=self.object.id)
            # userperfil.avatar=self.request.FILES['avatar']
            # userperfil.save()
        userperfil, created = Perfil.objects.get_or_create(user_id=self.object.id)
        if self.request.FILES:
            userperfil.avatar=self.request.FILES['avatar']
            userperfil.save()
        if self.request.POST:
            try: 
                userperfil.impresora=self.request.POST['impresora']
            except: pass
        userperfil.save()
        return super(UserUpdateView, self).form_valid(form)







class UserChgPasswordView(SuccessMessageMixin, UpdateView):
    template_name='autorizaciones/chgPassword.html'
    model=User
    form_class = chgPasswordForm
    # success_message = msg_render("El Password de %(username)s modificado con exito")
    # def get_success_url(self):
    #     return reverse_lazy('autorizaciones:det_usuario', args=(self.object.id, ))
    def get_success_url(self, instance):
        success_message = msg_render("El Password de <strong>(%s)</strong> Modificado con exito" % (str(instance.username) ))
        messages.success(self.request, success_message)
        url = reverse('autorizaciones:det_usuario', kwargs={'pk': instance.id})
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super(UserChgPasswordView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['usuario'] = self.object             
        return context
    
    def form_valid(self, form):
        usuario = User.objects.get(pk=self.object.id)
        usuario.set_password(self.request.POST['password'])
        usuario.save()
        #return super(UserChgPasswordView, self).form_valid(form)
        return self.get_success_url(usuario)




class UserDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=User
    success_url=reverse_lazy('autorizaciones:lst_usuario')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El usuario <strong>"+unicode(self.object.username)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))




class GroupUpdateView(SuccessMessageMixin, UpdateView):
    template_name='autorizaciones/updGroup.html'
    model=Group
    form_class = GroupForm
    success_message = msg_render("El grupo %(name)s modificado con exito")
    def get_success_url(self):
        return reverse_lazy('autorizaciones:det_grupo', args=(self.object.id, ))


class GroupCreateView(SuccessMessageMixin, CreateView):
    template_name='autorizaciones/addGroup.html'
    model = Group
    form_class = GroupForm
    success_message = msg_render("El grupo %(name)s registrado con exito")
    def get_success_url(self):
        return reverse_lazy('autorizaciones:det_grupo', args=(self.object.id, ))

class GroupDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=Group
    success_url=reverse_lazy('autorizaciones:lst_grupo')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El grupo <strong>"+unicode(self.object.name)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))




import requests  
from django.conf import settings  

class BaseJasperReport(object):
    report_name = ''
    filename = ''

    def __init__(self):
        self.auth = (settings.JASPER_USER, settings.JASPER_PASSWORD)
        super(BaseJasperReport, self).__init__()

    def get_report(self):
        url = '{url}/reports/{report_name}.pdf'.format(url=settings.JASPER_URL, report_name=self.report_name)
        req = requests.get(url, params=self.get_params(), auth=self.auth)

        return req.content

    def get_params(self):
        """
        Este metodo sera implementado por cada uno de nuestros reportes
        """
        raise NotImplementedError

    def render_to_response(self):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(self.filename)

        response.write(self.get_report())  #<_____

        return response



class UsuariosReport(BaseJasperReport):


    def __init__(self):
        self.filename = 'lista_de_usuarios'
        self.report_name = 'lista_usuarios'
        super(UsuariosReport, self).__init__()

    def get_params(self):
        return None

from django.views.generic import View
class DownloadScoresReport(View):
    def get(self, request, *args, **kwargs):


        report = UsuariosReport()
        return report.render_to_response()