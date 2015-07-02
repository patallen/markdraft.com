from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
#    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(
        r'^login/$',
        auth_views.login, 
        {'template_name': 'login.html'},
        name='login'
    ),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
]
