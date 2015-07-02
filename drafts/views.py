from django.views.generic.edit import CreateView, FormView
from registration.forms import RegistrationForm


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = RegistrationForm
    success_url = '/'
