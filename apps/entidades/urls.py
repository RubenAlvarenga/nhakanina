from django.conf.urls import patterns, url
from .views import PersonaSingleTableView, PersonaCreateView, PersonaDetailView, PersonaUpdateView, AlumnoSingleTableView, AlumnoCreateView, AlumnoDetailView, AlumnoUpdateView, PersonaDeleteView, AlumnoDeleteView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required

urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='base/divided.html'), name='entidades'),

    url(r'^personas/$', custom_permission_required('entidades.list_persona')(PersonaSingleTableView.as_view()), name ='lst_persona'),
    url(r'^personas/addPersona/$', custom_permission_required('entidades.add_persona')(PersonaCreateView.as_view()), name ='add_persona'),
    url(r'^personas/detPersona/(?P<pk>[\d]+)$', custom_permission_required('entidades.view_persona')(PersonaDetailView.as_view()), name ='det_persona'),
    url(r'^personas/updPersona/(?P<pk>[\d]+)$', custom_permission_required('entidades.change_persona')(PersonaUpdateView.as_view()), name ='upd_persona'),
    url(r'^personas/delPersona/(?P<pk>[\d]+)$', custom_permission_required('entidades.delete_persona')(PersonaDeleteView.as_view()), name ='del_persona'),


    url(r'^alumnos/$', custom_permission_required('entidades.list_alumno')(AlumnoSingleTableView.as_view()), name ='lst_alumno'),
    url(r'^alumnos/addAlumno/$', custom_permission_required('entidades.add_alumno')(AlumnoCreateView.as_view()), name ='add_alumno'),
    url(r'^alumnos/detAlumno/(?P<pk>[\d]+)$', custom_permission_required('entidades.view_alumno')(AlumnoDetailView.as_view()), name ='det_alumno'),
    url(r'^alumnos/updAlumno/(?P<pk>[\d]+)$', custom_permission_required('entidades.change_alumno')(AlumnoUpdateView.as_view()), name ='upd_alumno'),
    url(r'^alumnos/delAlumno/(?P<pk>[\d]+)$', custom_permission_required('entidades.delete_alumno')(AlumnoDeleteView.as_view()), name ='del_alumno'),
	
	url(r'^alumnos/verificarCedula-ajax/$', 'apps.entidades.views.verificarCedula_ajax' , name ='verificar_cedula'),

    url(r'^alumnos/get_full_name-ajax/$', 'apps.entidades.views.get_full_name_ajax' , name ='get_full_name'),
    url(r'^personas/get_full_name-ajax/$', 'apps.entidades.views.persona_get_full_name_ajax' , name ='persona_get_full_name'),

)








