from django.views.generic.edit import CreateView, FormView
from drafts.forms import LoginForm
from registration.forms import RegistrationForm


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'
    
    def form_valid(self, form):
        print("cookies")
        return super(LoginView, self).form_valid(form)


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = RegistrationForm
    success_url = '/'
