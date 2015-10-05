from django.conf.urls import patterns, url
from .views import ConceptoSingleTableView, ConceptoUpdateView, ConceptoDetailView, ConceptoCreateView, PeriodoSingleTableView, PeriodoCreateView, \
	PeriodoDetailView, ArancelSingleTableView, ArancelDetailView, ArancelCreateView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required


urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='base/divided.html'), name='aranceles'),

    url(r'^conceptos/$', custom_permission_required('aranceles.lst_concepto')(ConceptoSingleTableView.as_view()), name ='lst_concepto'),
	url(r'^conceptos/addConcepto/$', custom_permission_required('aranceles.add_concepto')(ConceptoCreateView.as_view()), name='add_concepto'),
    url(r'^conceptos/detConcepto/(?P<pk>[\d]+)$', custom_permission_required('aranceles.view_concepto')(ConceptoDetailView.as_view()), name='det_concepto'),
	url(r'^conceptos/updConcepto/(?P<pk>[\d]+)$', custom_permission_required('aranceles.change_concepto')(ConceptoUpdateView.as_view()), name='upd_concepto'),


    url(r'^periodos/$', custom_permission_required('aranceles.lst_periodo')(PeriodoSingleTableView.as_view()), name ='lst_periodo'),
	url(r'^periodos/addPeriodoArancel/$', custom_permission_required('aranceles.add_periodo')(PeriodoCreateView.as_view()), name='add_periodo'),
    url(r'^periodos/detPeriodo/(?P<pk>[\d]+)$', custom_permission_required('aranceles.view_periodo')(PeriodoDetailView.as_view()), name='det_periodo'),

    url(r'^aranceles/$', custom_permission_required('aranceles.lst_arancel')(ArancelSingleTableView.as_view()), name ='lst_arancel'),
	url(r'^aranceles/addArancel/$', custom_permission_required('aranceles.add_arancel')(ArancelCreateView.as_view()), name='add_arancel'),
    url(r'^aranceles/detArancel/(?P<pk>[\d]+)$', custom_permission_required('aranceles.view_arancel')(ArancelDetailView.as_view()), name='det_arancel'),

)