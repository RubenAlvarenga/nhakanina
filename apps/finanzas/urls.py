from django.conf.urls import patterns, url
from .views import AlumnoSingleTableView, PersonaSingleTableView,  AlumnoDetailView, PersonaDetailView, fraccionar_planpago_ajax, ReciboCancelView, \
    ReciboSingleTableView, ReciboFormView, PlanPagoFormView, ReciboPlanPagoFormView, ReciboDetailView, total_recibo_plan_pago_ajax, PlanPagoSingleTableView, \
    PlanPagoDetailView, PlanPagoUpdateView, PlanPagoDeleteView, CursoExtractoSingleTableView, CursoDetailView, FraccionarPlanFormView, EstadoDeCuentaSingleTableView
from apps.entidades.views import AlumnoCreateView
from apps.catedras.views import CursoCreateView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required


urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='base/divided.html'), name='finanzas'),

    url(r'^personas/$', custom_permission_required('finanzas.add_recibo')(PersonaSingleTableView.as_view()), name ='lst_persona'),
    url(r'^personas/detPersona/(?P<pk>[\d]+)$', custom_permission_required('finanzas.add_recibo')(PersonaDetailView.as_view()), name='det_persona'),
    url(r'^alumnos/detAlumno/(?P<pk>[\d]+)$', custom_permission_required('finanzas.view_planpago')(AlumnoDetailView.as_view()), name='det_alumno'),

    url(r'^estadoDeCuenta/$', custom_permission_required('finanzas.list_planpago')(EstadoDeCuentaSingleTableView.as_view()), name ='lst_estadoDeCuenta'),


    url(r'^fraccionar_planpago_ajax', 'apps.finanzas.views.fraccionar_planpago_ajax', name='fraccionar_planpago'),
    url(r'^total_recibo_plan_pago_ajax', 'apps.finanzas.views.total_recibo_plan_pago_ajax', name='total_recibo_plan_pago'),


    url(r'^recibos/$', custom_permission_required('finanzas.list_recibo')(ReciboSingleTableView.as_view()), name ='lst_recibo'),
    
    url(r'^recibos/anularRecibo/(?P<pk>[\d]+)$', custom_permission_required('finanzas.delete_recibo')(ReciboCancelView.as_view()), name ='anu_recibo'),

    #RECIBOS PLAN DE PAGO
    url(r'^recibos/genReciboPlanPago/$', ('apps.finanzas.views.genReciboPlanPago'), name ='gen_recibo_plan'),
    url(r'^recibos/addReciboPlanPago/$', custom_permission_required('finanzas.add_planpago')(ReciboPlanPagoFormView.as_view()), name ='add_recibo_plan'),


    #RECIBOS SUELTOS
    url(r'^recibos/genRecibo/$', ('apps.finanzas.views.genRecibo'), name ='gen_recibo'),
    url(r'^recibos/addRecibo/$', custom_permission_required('finanzas.add_recibo')(ReciboFormView.as_view()), name ='add_recibo'),
    url(r'^recibos/detRecibo/(?P<pk>[\d]+)$', custom_permission_required('finanzas.view_recibo')(ReciboDetailView.as_view()), name='det_recibo'),
    #A PLAN
    url(r'^planes/genPlanPago/$', ('apps.finanzas.views.genPlanPago'), name ='gen_planpago'),
    url(r'^planes/addPlanPago/$', custom_permission_required('finanzas.add_planpago')(PlanPagoFormView.as_view()), name ='add_planpago'),


    #ESPECIAL
    url(r'^alumnos/$', custom_permission_required('finanzas.list_alumno')(AlumnoSingleTableView.as_view()), name ='lst_alumno'),
    url(r'^personas/addPersona/$', custom_permission_required('entidades.add_alumno')(AlumnoCreateView.as_view()), name ='add_alumno'),


    url(r'^recibos/aplReciboPlanPago/(?P<pk>[\d]+)$', ('apps.finanzas.views.aplReciboPlanPago'), name ='apl_recibo_plan'),



    url(r'^planes/$', custom_permission_required('finanzas.list_planpago')(PlanPagoSingleTableView.as_view()), name ='lst_planpago'),

    url(r'^planes/detPlanPago/(?P<pk>[\d]+)$', custom_permission_required('finanzas.view_planpago')(PlanPagoDetailView.as_view()), name='det_planpago'),
    url(r'^planes/updPlanPago/(?P<pk>[\d]+)$', custom_permission_required('catedras.change_planpago')(PlanPagoUpdateView.as_view()), name='upd_planpago'),
    url(r'^planes/delPlanPago/(?P<pk>[\d]+)$', custom_permission_required('finanzas.delete_planpago')(PlanPagoDeleteView.as_view()), name ='del_planpago'),
    url(r'^planes/fraPlanPago/(?P<pk>[\d]+)$', custom_permission_required('finanzas.add_planpago')(FraccionarPlanFormView.as_view()), name='fra_planpago'),



    url(r'^get_curso_alumno_ajax', 'apps.finanzas.views.get_curso_alumno_ajax', name='get_cursoalumno'),
    url(r'^get_concepto_ajax', 'apps.finanzas.views.get_concepto_ajax', name='get_concepto'),
    url(r'^get_materias_ajax', 'apps.finanzas.views.get_materias_ajax', name='get_materias'),


    url(r'^cursos/$', custom_permission_required('catedras.list_cursos')(CursoExtractoSingleTableView.as_view()), name ='lst_curso'),
    url(r'^cursos/addCurso/$', custom_permission_required('catedras.add_curso')(CursoCreateView.as_view()), name ='add_curso'),
    url(r'^cursos/detCurso/(?P<pk>[\d]+)$', custom_permission_required('catedras.det_curso')(CursoDetailView.as_view()), name ='det_curso'),

    #imprimir
    url(r'^alumnos/prtExtracto/$', ('apps.finanzas.views.imprimirExtracto'), name ='prt_extracto'),

)


