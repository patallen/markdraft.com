from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from . import views
from drafts.decorators import anonymous_required

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='public/index.html'),
        name='index'
        ),
    url(r'^login/$',
        anonymous_required(auth_views.login),
        {'template_name': 'public/login.html'},
        name='login'
        ),
    url(r'^logout/$',
        login_required(auth_views.logout),
        {'next_page': '/'}, name='logout'
        ),
    url(r'^signup/$',
        anonymous_required(views.SignupView.as_view()),
        name='signup'
        ),
    url(r'^dashboard/$',
        login_required(views.DashboardView.as_view()),
        name='dashboard'),
    url(r'^create/$',
        views.CreateDocumentView.as_view(),
        name='create_document'
        ),
    url(r'^doc/(?P<hashid>\w{3,})/$',
        views.DocumentDetailView.as_view(),
        name='view_document'
        ),
    url(r'^doc/(?P<hashid>\w{3,})/edit/$',
        views.EditDocumentView.as_view(),
        name='edit_document'
        ),
]
