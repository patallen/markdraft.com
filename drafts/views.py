from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from registration.forms import RegistrationForm
from drafts.models import Document, Draft


class SignupView(CreateView):
    template_name = 'public/signup.html'
    form_class = RegistrationForm
    success_url = '/'


class DashboardView(ListView):
    template_name = 'drafts/dashboard.html'
    model = Draft

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(user=user)


class CreateDocumentView(CreateView):
    template_name = 'drafts/create.html'
    model = Draft
    fields = ['text']
    success_url = '/dashboard'

    def form_valid(self, form):
        doc = Document.objects.create(user=self.request.user)
        doc.update_hashid()
        doc.save()
        draft = form.save(commit=False)
        draft.document = doc
        draft.version = 1
        self.object = draft.save()
        return super(CreateDocumentView, self).form_valid(form)


class EditDocumentView(CreateDocumentView):
    template_name = 'drafts/edit.html'

    def get_initial(self):
        return {'text': self.document.latest_draft.text}

    def get_context_data(self, **kwargs):
        context = super(EditDocumentView, self).get_context_data(**kwargs)
        context['document'] = self.document
        return context

    def dispatch(self, *args, **kwargs):
        self.document = get_object_or_404(Document, hashid=kwargs['hashid'])
        return super(EditDocumentView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        draft = form.save(commit=False)
        draft.document = self.document
        draft.version = self.document.latest_draft.version + 1
        self.object = draft.save()
        return super(CreateView, self).form_valid(form)


class DocumentDetailView(DetailView):
    template_name = "drafts/view.html"
    model = Document
    slug_field = 'hashid'

    def get_object(self):
        return Document.objects.get(hashid=self.kwargs['hashid'])
