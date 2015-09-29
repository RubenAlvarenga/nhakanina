from django.conf.urls import patterns, url
from .views import UserSingleTableView, UserDetailView, GroupSingleTableView, GroupDetailView, UserDeleteView, GroupUpdateView, GroupCreateView, \
	GroupDeleteView, UserUpdateView, UserChgPasswordView, UserPerfilDetailView, UserPerfilUpdateView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base/divided.html'), name='autorizaciones'),

    url(r'^usuarios/$', custom_permission_required('auth.list_user')(UserSingleTableView.as_view()), name ='lst_usuario'),
    url(r'^usuarios/addUsuario/$', ('apps.autorizaciones.views.addUsuario'), name='add_usuario'),
    url(r'^usuarios/detUsuario/(?P<pk>[\d]+)$', custom_permission_required('auth.view_user')(UserDetailView.as_view()), name='det_usuario'),
	#url(r'^usuarios/updUsuario/(?P<pk>[\d]+)$', ('apps.autorizaciones.views.updUsuario'), name='upd_usuario'),
	url(r'^usuarios/updUsuario/(?P<pk>[\d]+)$', custom_permission_required('auth.change_user')(UserUpdateView.as_view()), name='upd_usuario'),
    url(r'^usuarios/delUsuario/(?P<pk>[\d]+)$', custom_permission_required('auth.delete_user')(UserDeleteView.as_view()), name='del_usuario'),
    url(r'^usuarios/chgPassword/(?P<pk>[\d]+)$', custom_permission_required('auth.change_user')(UserChgPasswordView.as_view()), name="chg_password"),

    url(r'^usuarios/detPerfil/(?P<pk>[\d]+)$', (UserPerfilDetailView.as_view()), name='det_miperfil'),
    url(r'^usuarios/updPerfil/(?P<pk>[\d]+)$', (UserPerfilUpdateView.as_view()), name='upd_miperfil'),

    url(r'^change-password/', auth_views.password_change, name='password_change'),

	url(r'^grupos/$', custom_permission_required('auth.list_group')(GroupSingleTableView.as_view()), name='lst_grupo'),
	url(r'^grupos/addGrupo/$', custom_permission_required('auth.add_group')(GroupCreateView.as_view()), name='add_grupo'),
    url(r'^grupos/detGrupo/(?P<pk>[\d]+)$', custom_permission_required('auth.view_group')(GroupDetailView.as_view()), name='det_grupo'),
	url(r'^grupos/updGrupo/(?P<pk>[\d]+)$', custom_permission_required('auth.change_group')(GroupUpdateView.as_view()), name='upd_grupo'),
    url(r'^grupos/delGrupo/(?P<pk>[\d]+)$', custom_permission_required('auth.delete_group')(GroupDeleteView.as_view()), name='del_grupo'),

)

