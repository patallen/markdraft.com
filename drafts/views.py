from django.views.generic.edit import CreateView, FormView
from drafts.forms import LoginForm
from registration.forms import RegistrationForm


class IndexView(FormView):
    form_class = LoginForm
    template_name = 'index.html'
    success_url = '/'


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = RegistrationForm
    success_url = '/'
