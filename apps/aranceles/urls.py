from django.conf.urls import patterns, url
from .views import ConceptoSingleTableView, ConceptoUpdateView, ConceptoDetailView, ConceptoCreateView, PeriodoSingleTableView, PeriodoCreateView, \
	PeriodoDetailView, ArancelSingleTableView, ArancelDetailView, ArancelCreateView, TipoConceptoSingleTableView, TipoConceptoDetailView, TipoConceptoCreateView, \
    TipoConceptoUpdateView, TipoConceptoDeleteView, PeriodoUpdateView, PeriodoDeleteView, ConceptoDeleteView, ArancelUpdateView, ArancelDeleteView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required


urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='base/divided.html'), name='aranceles'),

    url(r'^conceptos/$', custom_permission_required('aranceles.list_concepto')(ConceptoSingleTableView.as_view()), name ='lst_concepto'),
	url(r'^conceptos/addConcepto/$', custom_permission_required('aranceles.add_concepto')(ConceptoCreateView.as_view()), name='add_concepto'),
    url(r'^conceptos/detConcepto/(?P<pk>[\d]+)$', custom_permission_required('aranceles.view_concepto')(ConceptoDetailView.as_view()), name='det_concepto'),
	url(r'^conceptos/updConcepto/(?P<pk>[\d]+)$', custom_permission_required('aranceles.change_concepto')(ConceptoUpdateView.as_view()), name='upd_concepto'),
    url(r'^conceptos/delConcepto/(?P<pk>[\d]+)$', custom_permission_required('aranceles.delete_concepto')(ConceptoDeleteView.as_view()), name ='del_concepto'),


    url(r'^periodos/$', custom_permission_required('aranceles.list_periodo')(PeriodoSingleTableView.as_view()), name ='lst_periodo'),
    url(r'^periodos/addPeriodo/$', custom_permission_required('aranceles.add_periodo')(PeriodoCreateView.as_view()), name='add_periodo'),
    url(r'^periodos/detPeriodo/(?P<pk>[\d]+)$', custom_permission_required('aranceles.view_periodo')(PeriodoDetailView.as_view()), name='det_periodo'),
    url(r'^periodos/updPeriodo/(?P<pk>[\d]+)$', custom_permission_required('aranceles.change_periodo')(PeriodoUpdateView.as_view()), name='upd_periodo'),
    url(r'^periodos/delPeriodo/(?P<pk>[\d]+)$', custom_permission_required('aranceles.delete_periodo')(PeriodoDeleteView.as_view()), name ='del_periodo'),


    url(r'^aranceles/$', custom_permission_required('aranceles.list_arancel')(ArancelSingleTableView.as_view()), name ='lst_arancel'),
	url(r'^aranceles/addArancel/$', custom_permission_required('aranceles.add_arancel')(ArancelCreateView.as_view()), name='add_arancel'),
    url(r'^aranceles/detArancel/(?P<pk>[\d]+)$', custom_permission_required('aranceles.view_arancel')(ArancelDetailView.as_view()), name='det_arancel'),
    url(r'^aranceles/updArancel/(?P<pk>[\d]+)$', custom_permission_required('aranceles.change_arancel')(ArancelUpdateView.as_view()), name='upd_arancel'),
    url(r'^aranceles/delArancel/(?P<pk>[\d]+)$', custom_permission_required('aranceles.delete_arancel')(ArancelDeleteView.as_view()), name ='del_arancel'),
    

    url(r'^tipos/$', custom_permission_required('aranceles.list_tipoconcepto')(TipoConceptoSingleTableView.as_view()), name ='lst_tipoconcepto'),
    url(r'^tipos/detTipoConcepto/(?P<pk>[\d]+)$', custom_permission_required('aranceles.view_tipoconcepto')(TipoConceptoDetailView.as_view()), name='det_tipoconcepto'),
    url(r'^tipos/addTipoConcepto/$', custom_permission_required('aranceles.add_tipoconcepto')(TipoConceptoCreateView.as_view()), name='add_tipoconcepto'),
    url(r'^tipos/updTipoConcepto/(?P<pk>[\d]+)$', custom_permission_required('aranceles.change_tipoconcepto')(TipoConceptoUpdateView.as_view()), name='upd_tipoconcepto'),
    url(r'^tipos/delTipoConcepto/(?P<pk>[\d]+)$', custom_permission_required('aranceles.delete_tipoconcepto')(TipoConceptoDeleteView.as_view()), name ='del_tipoconcepto'),


)