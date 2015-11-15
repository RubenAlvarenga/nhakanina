from django.conf.urls import patterns, url
from .views import CursoSingleTableView, CursoDetailView, CursoCreateView, CursoUpdateView, CursoAlumnoCreateView, CarreraSingleTableView, CarreraCreateView, \
	CarreraDetailView, CarreraUpdateView, CarreraDeleteView, MateriaSingleTableView, MateriaDetailView, MateriaCreateView, MateriaUpdateView, \
    MateriaDeleteView, CursoDeleteView, CursoAlumnoSingleTableView, CursoAlumnoDetailView, CursoAlumnoUpdateView, CursoAlumnoDeleteView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required


urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='base/divided.html'), name='catedras'),

    url(r'^cursos/$', custom_permission_required('catedras.list_curso')(CursoSingleTableView.as_view()), name ='lst_curso'),
    url(r'^cursos/detCurso/(?P<pk>[\d]+)$', custom_permission_required('catedras.view_curso')(CursoDetailView.as_view()), name='det_curso'),
    url(r'^cursos/addCurso/$', custom_permission_required('catedras.add_curso')(CursoCreateView.as_view()), name ='add_curso'),
    url(r'^cursos/updCurso/(?P<pk>[\d]+)$', custom_permission_required('catedras.change_curso')(CursoUpdateView.as_view()), name='upd_curso'),
    url(r'^cursos/delCurso/(?P<pk>[\d]+)$', custom_permission_required('catedras.delete_curso')(CursoDeleteView.as_view()), name='del_curso'),

    url(r'^matriculaciones/$', custom_permission_required('catedras.list_cursoalumno')(CursoAlumnoSingleTableView.as_view()), name ='lst_curso_alumno'),
    url(r'^matriculaciones/addCursoAlumno/$', custom_permission_required('catedras.add_cursoalumno')(CursoAlumnoCreateView.as_view()), name ='add_curso_alumno'),
    url(r'^matriculaciones/addMatricula/$', custom_permission_required('catedras.add_cursoalumno')(CursoAlumnoCreateView.as_view()),),

    url(r'^matriculaciones/detCursoAlumno/(?P<pk>[\d]+)$', custom_permission_required('catedras.view_cursoalumno')(CursoAlumnoDetailView.as_view()), name ='det_curso_alumno'),
    url(r'^matriculaciones/updCursoAlumno/(?P<pk>[\d]+)$', custom_permission_required('catedras.change_cursoalumno')(CursoAlumnoUpdateView.as_view()), name ='upd_curso_alumno'),
    url(r'^matriculaciones/delCursoAlumno/(?P<pk>[\d]+)$', custom_permission_required('catedras.delete_cursoalumno')(CursoAlumnoDeleteView.as_view()), name ='del_curso_alumno'),

    url(r'^cursos/recuperarPlan/(?P<pk>[\d]+)$', ('apps.catedras.views.recuperarPlan'), name='recuperar_plan'),

    url(r'^carreras/$', custom_permission_required('catedras.list_carrera')(CarreraSingleTableView.as_view()), name ='lst_carrera'),
    url(r'^carreras/detCarrera/(?P<pk>[\d]+)$', custom_permission_required('catedras.view_carrera')(CarreraDetailView.as_view()), name='det_carrera'),
    url(r'^carreras/addCarrera/$', custom_permission_required('catedras.add_carrera')(CarreraCreateView.as_view()), name ='add_carrera'),
    url(r'^carreras/updCarrera/(?P<pk>[\d]+)$', custom_permission_required('catedras.change_carrera')(CarreraUpdateView.as_view()), name='upd_carrera'),
    url(r'^carreras/delCarrera/(?P<pk>[\d]+)$', custom_permission_required('catedras.delete_carrera')(CarreraDeleteView.as_view()), name='del_carrera'),

    url(r'^materias/$', custom_permission_required('catedras.list_materia')(MateriaSingleTableView.as_view()), name ='lst_materia'),
    url(r'^materias/detMateria/(?P<pk>[\d]+)$', custom_permission_required('catedras.view_materia')(MateriaDetailView.as_view()), name='det_materia'),
    url(r'^materias/addMateria/$', custom_permission_required('catedras.add_materia')(MateriaCreateView.as_view()), name ='add_materia'),
    url(r'^materias/updMateria/(?P<pk>[\d]+)$', custom_permission_required('catedras.change_materia')(MateriaUpdateView.as_view()), name='upd_materia'),
    url(r'^materias/delMateria/(?P<pk>[\d]+)$', custom_permission_required('catedras.delete_materia')(MateriaDeleteView.as_view()), name='del_materia'),

    url(r'^cursos/get_full_curso_ajax/$', 'apps.catedras.views.get_full_curso_ajax' , name ='get_full_curso'),

)


