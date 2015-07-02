from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from registration.forms import RegistrationForm


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = RegistrationForm
    success_url = '/'


class DashboardView(TemplateView):
    template_name = 'dashboard.html'
