from django.conf.urls import patterns, url
from .views import DescuentoSingleTableView, DescuentoCreateView, DescuentoDetailView, DescuentoUpdateView, DescuentoDeleteView

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required


urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='base/divided.html'), name='descuentos'),
    url(r'^descuentos/$', custom_permission_required('descuentos.add_PorTipoCarreraConcepto')(DescuentoSingleTableView.as_view()), name ='lst_descuento'),
    url(r'^descuentos/addDescuento/$', custom_permission_required('descuentos.add_descuento')(DescuentoCreateView.as_view()), name='add_descuento'),
    url(r'^descuentos/detDescuento/(?P<pk>[\d]+)$', custom_permission_required('descuentos.view_descuento')(DescuentoDetailView.as_view()), name='det_descuento'),
	url(r'^descuentos/updDescuento/(?P<pk>[\d]+)$', custom_permission_required('descuentos.change_descuento')(DescuentoUpdateView.as_view()), name='upd_descuento'),
    url(r'^descuentos/delDescuento/(?P<pk>[\d]+)$', custom_permission_required('descuentos.delete_descuento')(DescuentoDeleteView.as_view()), name ='del_descuento'),

)


