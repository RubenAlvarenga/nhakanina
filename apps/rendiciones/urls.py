from django.conf.urls import patterns, url
from .views import RendicionSingleTableView, RendicionCreateView, RendicionDetailView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required


urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='base/divided.html'), name='rendiciones'),

    url(r'^rendiciones/$', custom_permission_required('rendiciones.lst_rendicion')(RendicionSingleTableView.as_view()), name ='lst_rendicion'),
    url(r'^rendiciones/addRendicion/$', custom_permission_required('rendiciones.add_rendicion')(RendicionCreateView.as_view()), name='add_rendicion'),
    url(r'^rendiciones/detRendicion/(?P<pk>[\d]+)$', custom_permission_required('rendiciones.view_rendicion')(RendicionDetailView.as_view()), name='det_rendicion'),

)