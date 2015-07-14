from django.shortcuts import get_object_or_404
from django.http import HttpResponse 
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from registration.forms import RegistrationForm
from drafts.models import Document, Draft
from drafts.forms import HorizontalRegForm
from rest_framework import generics
from drafts.serializers import DocumentSerializer


class SignupView(CreateView):
    template_name = 'public/signup.html'
    form_class = RegistrationForm
    success_url = '/dashboard'


class IndexView(SignupView):
    template_name = 'public/index.html'
    form_class = HorizontalRegForm


class DashboardView(ListView):
    template_name = 'drafts/dashboard.html'
    model = Draft

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(user=user)


class CreateDocumentView(CreateView):
    template_name = 'drafts/edit.html'
    model = Draft
    fields = ['title', 'text']
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
        return {
            'title': self.document.latest_draft.title,
            'text': self.document.latest_draft.text
        }

    def get_context_data(self, **kwargs):
        context = super(EditDocumentView, self).get_context_data(**kwargs)
        context['document'] = self.document
        return context

    def dispatch(self, *args, **kwargs):
        self.document = get_object_or_404(Document, hashid=kwargs['hashid'])
        return super(EditDocumentView, self).dispatch(*args, **kwargs)

    def form_invalid(self, form):
        print(form.errors)
        return super(CreateDocumentView, self).form_invalid(form)

    def form_valid(self, form):
        draft = form.save(commit=False)
        draft.document = self.document
        draft.version = self.document.latest_draft.version + 1
        self.object = draft.save()
        return super(CreateDocumentView, self).form_valid(form)


class DocumentDetailView(DetailView):
    template_name = "drafts/view.html"
    model = Document
    slug_field = 'hashid'

    def get_object(self):
        return Document.objects.get(hashid=self.kwargs['hashid'])


class DocumentListResource(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(user=user)


class AjaxStarView(View):

    def post(self, request, *args, **kwargs):
        doc = get_object_or_404(Document, hashid=request.POST['hashid'])
        if doc.user != request.user:
            return HttpResponse('Not authorized to star that.', 401)

        doc.starred = not doc.starred 
        doc.save()
        return HttpResponse('Starring successful.', 200)
    

