from django.views.generic.edit import CreateView
from django.views.generic import ListView
from registration.forms import RegistrationForm
from drafts.models import Document, Draft


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


class CreateDocumentView(CreateView):
    template_name = 'create.html'
    model = Draft
    fields = ['text']
    success_url = '/'

    def form_valid(self, form):
        doc = Document(user=self.request.user)
        doc.save()
        draft = form.save(commit=False)
        draft.document = doc
        draft.version = 1
        self.object = draft.save()
        return super(CreateView, self).form_valid(form)
