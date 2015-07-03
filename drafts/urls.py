from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^dashboard/$',
        login_required(views.DashboardView.as_view()),
        name='dashboard'),
    url(r'^create/$', views.CreateDocumentView.as_view(), name='create_document'),
    url(r'^doc/(?P<hashid>[\w{}.-]{3})/$', views.DocumentDetailView.as_view(), name='view_document'),
]
