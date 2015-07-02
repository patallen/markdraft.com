from django.views.generic.edit import CreateView
from django.views.generic import ListView
from registration.forms import RegistrationForm
from drafts.models import Document


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = RegistrationForm
    success_url = '/'


class DashboardView(ListView):
    template_name = 'dashboard.html'
    model = Draft

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(user=user)
